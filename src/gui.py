from knots_new import *
from parameterizations import *
from visualize_distortion import *

from traits.api import HasTraits, Range, Instance, Bool, Int, Float, Enum, observe
from traitsui.api import View, Item, Group, HSplit, VSplit, Tabbed

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, \
    MlabSceneModel, DecoratedScene


class StickKnotVisualiser(HasTraits):
    knot = Instance(StickKnot)
    minimum_thickness = Range(0., 1., 0.05)
    vary_thickness_by_distortion = Bool
    colormap = Enum("hsv", "spring", "summer", "winter", "autumn", "cool")
    colorbar = Bool
    point_1 = Range(0., 1., 0)
    point_2 = Range(0., 1., 0.5)
    index1 = Int
    index2 = Int
    distortion_ratio = Float
    highlight_vertex_distortion = Bool

    scene = Instance(MlabSceneModel, ())
    torus_scene = Instance(MlabSceneModel, ())

    knot_plot = Instance(PipelineBase)
    torus_plot = Instance(PipelineBase)
    peaks_plot = Instance(PipelineBase)
    point_markers = Instance(PipelineBase)


    def get_markersXYZ(self):
        self.index1 = int(np.floor(self.point_1 * self.knot.num_vertices))
        self.index2 = int(np.floor(self.point_2 * self.knot.num_vertices))
        if self.index1 >= self.knot.num_vertices:
            self.index1 -= self.knot.num_vertices
        if self.index2 >= self.knot.num_vertices:
            self.index2 -= self.knot.num_vertices
        point1xyz = self.knot.vertices[self.index1]
        point2xyz = self.knot.vertices[self.index2]
        return np.array([point1xyz, point2xyz]).T

    @observe('minimum_thickness,vary_thickness_by_distortion,colorbar,colormap,highlight_vertex_distortion,scene.activated')
    def update_knot_plot(self, event=None):
        if self.knot_plot is None:
            self.knot_plot = self.knot.plot(scene_mlab=self.scene.mlab)
        else:
            # print("Reached else", flush=True)
            self.knot_plot.parent.parent.filter.radius = self.minimum_thickness
        if self.point_markers is None:
            self.point_markers = self.scene.mlab.points3d(*self.get_markersXYZ(), [0, 1], scale_mode="none", colormap="binary")
            self.distortion_ratio = self.knot.distortion_ratios[self.knot.mode][self.index1][self.index2]
        if self.vary_thickness_by_distortion:
            self.knot_plot.mlab_source.trait_set(scalars=self.knot.highest_distortion_ratio_of_vertex_loop)
            self.knot_plot.parent.parent.filter.vary_radius = "vary_radius_by_scalar"
        else:
            self.knot_plot.mlab_source.trait_set(scalars=self.knot.default_plot_scalars)
        if self.colorbar:
            if self.vary_thickness_by_distortion:
                self.scene.mlab.colorbar(object=self.knot_plot, title="Highest Distortion Ratio of Vertex", orientation="horizontal")
            else:
                self.scene.mlab.colorbar(object=self.knot_plot, title="Position", orientation="horizontal")
        if self.highlight_vertex_distortion:
            num_pairs = self.knot.vertex_distortion_pairs.shape[0]
            point_indices = np.copy(self.knot.vertex_distortion_pairs).flatten()
            points = self.knot.vertices[point_indices]
            scalars = np.array([np.arange(num_pairs), np.arange(num_pairs)]).T.flatten()
            self.scene.mlab.points3d(*(points.T), scalars, scale_mode="none", scale_factor=2, mode="cube")

        self.knot_plot.module_manager.scalar_lut_manager.lut_mode = self.colormap
        mlab.get_engine().scenes[0].scene.do_render = True


    @observe('torus_scene.activated')
    def update_torus_plot(self, event=None):
        self.torus_plot, self.peaks_plot = visualize_distortion(self.knot, plot_knot=False, cmap="gist_earth", highlight_peaks=True, scene_mlab=self.torus_scene.mlab)


    @observe('point_1,point_2')
    def update_distortion_ratio(self, event=None):
        pointsX, pointsY, pointsZ = self.get_markersXYZ()
        if self.point_markers is not None:
            self.point_markers.mlab_source.trait_set(x=pointsX, y=pointsY, z=pointsZ)
        self.distortion_ratio = self.knot.distortion_ratios[self.knot.mode][self.index1][self.index2]


    # The layout of the dialog created
    control_panel = Tabbed(
                        Group(Item(name="minimum_thickness"), Item(name="colorbar"), Item(name="colormap"), label="Knot Graphics", show_border=True),
                        Group(Item(name="point_1"), Item(name="point_2"), Item(name="distortion_ratio", style="readonly"), label="Point Picker", show_border=True),
                        Group(Item(name="highlight_vertex_distortion"), Item(name="vary_thickness_by_distortion"), label="Distortion Analysis", show_border=True)
                    )
    embedded_knot_plot = Item('scene', editor=SceneEditor(scene_class=DecoratedScene),
                         height=768, width=683, show_label=False)
    embedded_torus_plot = Item('torus_scene', editor=SceneEditor(scene_class=DecoratedScene),
                         height=550, width=683, show_label=False)
    view = View(HSplit(VSplit(control_panel, embedded_torus_plot), embedded_knot_plot), resizable=True, height=768, width=1366)


if __name__ == "__main__":
    DIRECTIONS = get_knot_point_cloud("smooth_figure8", 5, 1500)
    K = StickKnot(DIRECTIONS, validate=False, compute_distortion=True, mode="euclidean")
    visualiser = StickKnotVisualiser(knot=K)
    visualiser.configure_traits()
