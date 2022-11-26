var viewport_shape = [0,0]

var set_viewport_size = function() {
    canva_view = document.getElementById("viewport");
    canva_view.width = canva_view.clientWidth;
    canva_view.height = canva_view.clientHeight;
    viewport_shape = [canva_view.clientWidth, canva_view.clientHeight]
}

set_viewport_size()

addEventListener("resize", (event) => {
    set_viewport_size();
});