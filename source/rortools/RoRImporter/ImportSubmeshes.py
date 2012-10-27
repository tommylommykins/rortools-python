#TODO: Submesh arguments
import functools
from Py3dsMax import mxs

class SubmeshTracker(object):
    def __init__(self, submeshes, cabs, texcoords, backmeshes):
        self.submeshes = sorted(submeshes)
        self.cabs = cabs
        self.texcoords = texcoords
        self.backmeshes = sorted(backmeshes)
        
    def each_submesh(self):
        """yields a sequence of ImportationSubmesh objects, for all the submeshes seen in the truck file.
        """
        for submesh_line_no in self.submeshes:
            filter_fun = functools.partial(self._things_in_applicable_submesh, submesh_line_no)
            the_cabs = filter(filter_fun, self.cabs)
            the_texcoords = filter(filter_fun, self.texcoords)
            the_backmesh = False
            for backmesh_line_no in self.backmeshes:
                if self._applicable_submesh(backmesh_line_no) == submesh_line_no:
                    the_backmesh = True
            yield ImportationSubmesh(the_cabs, the_texcoords, the_backmesh)
            
    def _things_in_applicable_submesh(self, applicable_submesh, thing):
        """Thing must be indexable by 'line'.
        Returns all elements in thing whose applicable submesh is the same as the supplied
        applicable submesh.
        """
        return self._applicable_submesh(thing['line']) == applicable_submesh
        
    def _applicable_submesh(self, line_no):
        """Retrns the line number of the nearest-above submesh declaration to this point.
        This will uniquely identify the submesh which any other item belongs to. 
        """
        current_submesh = 0
        for submesh in self.submeshes:
            if submesh > line_no:
                return current_submesh
            current_submesh = submesh
            
class ImportationSubmesh(object):
    def __init__(self, cabs, texcoords, backmesh):
        self.cabs = cabs
        self.texcoords = texcoords
        self.backmesh = backmesh
            
def import_submeshes(node_positions, submeshes, cabs, texcoords, backmeshes, object_holder):
    tracker = SubmeshTracker(submeshes, cabs, texcoords, backmeshes)
    for i, submesh in enumerate(tracker.each_submesh()):
        _import_submesh(i, node_positions, submesh, object_holder)
        
def _import_submesh(index, node_positions, submesh, object_holder):
    if len(submesh.cabs) == 0:
        return
    max_positions = map(lambda node_position: node_position.to_point3(), node_positions)
    max_faces = []
    for cab in submesh.cabs:
        max_faces.append(mxs.point3(cab['node1'] + 1, cab['node2'] + 1, cab['node3'] + 1))
    mesh = mxs.mesh(vertices=max_positions, faces=max_faces)
    mesh.wirecolor = mxs.point3(55, 55, 83)
    mesh.name = "submesh_" + str(index)
    mxs.meshop.deleteisoverts(mesh)
    object_holder.add_object(mesh)
    mxs.custattributes.add(mesh, mxs.rorsubmesh)
    mesh.backmesh = submesh.backmesh
    for cab in submesh.cabs:
        if 'args' in cab:
            mesh.flag = cab['args']
            break

    