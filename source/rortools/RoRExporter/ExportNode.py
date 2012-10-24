from Py3dsMax import mxs

from blur3d.api import Scene

from .._global import Node

import ExportBeam

class FilteredNodeSet(object):
    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.nodes = []
        
    def add_node(self, candidate_node):
        distances = map(lambda other_node: candidate_node.distance_to(other_node), self.nodes)
        nodes_too_close = filter(lambda distance: self.max_distance >= distance, distances)
        separation_categories = self._separation_categories(candidate_node)
        if not separation_categories:
            if len(nodes_too_close) == 0:
                self.nodes.append(candidate_node)
        else:
            pass
        
    def _separation_categories(self, node):
        """Gets a set of separation categories for a node, if they are near separation boxes"""
        #node separation only occurs where separation boxes, so if node is not near one, then return no separation categories
        if not self._node_near_separation_box(node):
            return set()
        separation_categories = self._separation_categories_ignoring_separation_boxes(node)
        ret = separation_categories
        if len(ret) == 0:
            return set()
        print self._node_near_separation_box(node)
        print ret
        return ret

    def _node_near_separation_box(self, node):
        """Gets if a node is near a separation box"""
        separation_boxes = self._separation_boxes()
        distances = map(lambda sep_box: node.distance_to(sep_box), separation_boxes)
        boxes_near_enough = filter(lambda distance: distance < 0.1, distances)
        return any(boxes_near_enough)
    
    def _separation_boxes(self):
        """Gets all the separation boxes in the scene as a list of Nodes"""
        if not hasattr(self, "_internal_separation_boxes"):
            sep_boxes = filter(lambda obj: obj.name().lower().startswith("separation_node"),
                               Scene.instance().objects())
            map(lambda box: mxs.centerpivot(box._nativePointer), sep_boxes)
            self._internal_separation_boxes = map(lambda obj: Node.Node(obj._nativePointer.pos),
                                                  sep_boxes)
        return self._internal_separation_boxes
    
    def _beam_objects(self):
        """Gets all the beam objects in the scene"""
        if not hasattr(self, "_internal_beam_objects"):
            self._internal_beam_objects = \
                map(lambda obj: ExportBeam.Beam(obj._nativePointer, []),
                    filter(lambda obj: obj.name().lower().startswith("beam_"),
                           Scene.instance().objects()))
        return self._internal_beam_objects
    
    def _separation_categories_ignoring_separation_boxes(self, node):
        """Gets all the separation categories for beam objects which are
        coincident at this point, ignoring the presence of a separation node or not"""
        all_found_categories = set()
        for beam_object in self._beam_objects():
            max_object = beam_object.max_object
            if max_object.sepcat_one.strip() is "" and max_object.sepcat_two.strip() is "":
                continue
            nodes_at_position = map(lambda candidate_node: node.distance_to(candidate_node) < self.max_distance,
                                    beam_object.all_nodes())
            if not any(nodes_at_position):
                continue
            if max_object.sepcat_one.strip() is not "":
                all_found_categories.add(max_object.sepcat_one)
            if max_object.sepcat_two.strip() is not "":
                all_found_categories.add(max_object.sepcat_two)
        return set(sorted(all_found_categories))
        
        
class NodeExporter(object):
    def __init__(self, beam_objs):
        beam_objs = map(lambda beam: ExportBeam.Beam(beam, []), beam_objs)
        unfiltered_nodes = self._read_nodes(beam_objs)
        node_set = FilteredNodeSet(0.02)
        for node in unfiltered_nodes:
            node_set.add_node(node)
            
        self.nodes =  node_set.nodes
        self.node_positions = self._generate_node_positions()
        
        for node in self.nodes:
            categories = node_set._separation_categories(node)
            if not categories: continue
            print node
            print categories
            print "-" * 80
        
    def _generate_node_positions(self):
        the_lambda = lambda node: lambda node: mxs.point3(node.x, node.y, node.z)
        return map(the_lambda, self.nodes)
            
    def render_nodes(self):
        ret = "nodes\n"
        for i, node in enumerate(self.nodes):
            ret += str(i) + ", " + str(node.x) + ", " + str(node.y) + ", " + str(node.z) + "\n"
        return ret
    
    #===========================================================================
    # def _annotate_unfiltered_nodes(self, nodes):
    #    """Returns a list of tuples, where the first element is node
    #    and the second node is whether it is a separation node or not"""
    #    annotated_nodes = []
    
    #    for node in nodes:
    #        sep_node_distances = map(lambda sep_node: node.distance_to(sep_node),
    #                                 separation_nodes)
    #        sep_nodes_within_range = filter(lambda distance: distance < 0.02,
    #                                        sep_node_distances)
    #        sep_nodes_found = len(sep_nodes_within_range) > 0
    #        annotated_nodes.append((node, sep_nodes_found))
    #    return annotated_nodes
    #===========================================================================

    def _read_nodes(self, beam_objs):
        """get a list of nodes that form part of each beam object.
        Nodes which terminate at the same place have not yet been deleted...
        This is literally a list of all the knots which are at a certain point""" 
        knots = []
        for beam_obj in beam_objs:
            beam_obj = beam_obj.max_object
            for spline_no in range(mxs.numsplines(beam_obj)):
                spline_no += 1
                for knot_no in range(mxs.numknots(beam_obj, spline_no)):
                    knot_no += 1
                    knots.append(str(mxs.getKnotPoint(beam_obj, spline_no, knot_no)))
        node_list = []
        for knot in knots:
            node_list.append(Node.Node(knot))
        return sorted(node_list)