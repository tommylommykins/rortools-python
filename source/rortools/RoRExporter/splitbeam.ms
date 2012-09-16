fn SplitBeam BeamName = --Splits an editable spline into one-segment long splines
(
    --Run through all *original* splines in the object
    for i = 1 to numsplines BeamName do
    (
        local NewSplineCounter = numsplines BeamName -- Forms an index for working with new splines
        local ClosedTest = isclosed BeamName i
        Local FirstLinkingKnot, SecondLinkingKnot
        if closedtest == true then -- Get the coordinates of the points of the 'closing' segment, so it can be reconstructed later
        (
            open BeamName i
            Local FirstLinkingKnot  = getKnotPoint BeamName i 1
            Local SecondLinkingKnot = getKnotPoint BeamName i (numknots BeamName i)
        )           
        while numsegments BeamName i > 1 do
        (
            NewSplineCounter = NewSplineCounter + 1 --Update index
            addnewspline BeamName
            AddKnot BeamName NewSplineCounter #corner #line (getKnotPoint BeamName i 1) --Create new spline at location of first segment of old spline
            AddKnot BeamName NewSplineCounter #corner #line (getKnotPoint BeamName i 2)
            deleteKnot BeamName i 1 --Delete the same segment as the new spline of the old spline
        )
        if ClosedTest == true then -- Add the closing segment
        (
            addnewspline BeamName
            NewSplineCounter = NewSplineCounter + 1
            AddKnot BeamName NewSplineCounter #corner #line (FirstLinkingKnot)
            AddKnot BeamName NewSplineCounter #corner #line (SecondLinkingKnot)
        )
    )
    updateshape BeamName
)