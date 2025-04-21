// File: src/trianglengin/cpp/bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
#include <pybind11/functional.h> // Needed for std::function with optional
#include <vector>
#include <stdexcept>
#include <cstring>  // For memcpy with int8_t
#include <optional> // Include optional

#include "game_state.h"
#include "config.h"
#include "structs.h"

namespace py = pybind11;
namespace tg = trianglengin::cpp;

// Helper to convert Python EnvConfig to C++ EnvConfigCpp
tg::EnvConfigCpp python_to_cpp_env_config(const py::object &py_config)
{
  tg::EnvConfigCpp cpp_config;
  try
  {
    cpp_config.rows = py_config.attr("ROWS").cast<int>();
    cpp_config.cols = py_config.attr("COLS").cast<int>();
    cpp_config.num_shape_slots = py_config.attr("NUM_SHAPE_SLOTS").cast<int>();

    py::list py_ranges = py_config.attr("PLAYABLE_RANGE_PER_ROW").cast<py::list>();
    cpp_config.playable_range_per_row.clear();
    cpp_config.playable_range_per_row.reserve(py_ranges.size());
    for (const auto &item : py_ranges)
    {
      py::tuple range_tuple = item.cast<py::tuple>();
      if (range_tuple.size() != 2)
        throw std::runtime_error("Playable range tuple must have 2 elements.");
      cpp_config.playable_range_per_row.emplace_back(range_tuple[0].cast<int>(), range_tuple[1].cast<int>());
    }
    if (cpp_config.playable_range_per_row.size() != static_cast<size_t>(cpp_config.rows))
    {
      throw std::runtime_error("Mismatch between ROWS and PLAYABLE_RANGE_PER_ROW length.");
    }

    cpp_config.reward_per_placed_triangle = py_config.attr("REWARD_PER_PLACED_TRIANGLE").cast<double>();
    cpp_config.reward_per_cleared_triangle = py_config.attr("REWARD_PER_CLEARED_TRIANGLE").cast<double>();
    cpp_config.reward_per_step_alive = py_config.attr("REWARD_PER_STEP_ALIVE").cast<double>();
    cpp_config.penalty_game_over = py_config.attr("PENALTY_GAME_OVER").cast<double>();
    cpp_config.action_dim = cpp_config.num_shape_slots * cpp_config.rows * cpp_config.cols;
  }
  catch (const py::error_already_set &e)
  {
    throw std::runtime_error(std::string("Error accessing EnvConfig attributes: ") + e.what());
  }
  catch (const std::exception &e)
  {
    throw std::runtime_error(std::string("Error converting EnvConfig: ") + e.what());
  }
  return cpp_config;
}

// Helper to convert C++ optional<ShapeCpp> to Python tuple or None
py::object cpp_shape_to_python(const std::optional<tg::ShapeCpp> &shape_opt)
{
  if (!shape_opt)
    return py::none();
  const auto &shape = shape_opt.value();
  py::list triangles_py;
  for (const auto &tri : shape.triangles)
  {
    triangles_py.append(py::make_tuple(std::get<0>(tri), std::get<1>(tri), std::get<2>(tri)));
  }
  py::tuple color_py = py::make_tuple(std::get<0>(shape.color), std::get<1>(shape.color), std::get<2>(shape.color));
  return py::make_tuple(triangles_py, color_py, shape.color_id);
}

// Helper to convert Python tuple (or None) to C++ optional<ShapeCpp>
std::optional<tg::ShapeCpp> python_to_cpp_shape(const py::object &shape_py)
{
  if (shape_py.is_none())
  {
    return std::nullopt;
  }
  try
  {
    py::tuple shape_tuple = shape_py.cast<py::tuple>();
    if (shape_tuple.size() != 3)
    {
      throw std::runtime_error("Shape tuple must have 3 elements (triangles, color, id).");
    }

    py::list tris_py = shape_tuple[0].cast<py::list>();
    py::tuple color_py = shape_tuple[1].cast<py::tuple>();
    int id_py = shape_tuple[2].cast<int>();

    std::vector<tg::TriangleData> tris_cpp;
    tris_cpp.reserve(tris_py.size());
    for (const auto &tri_item : tris_py)
    {
      py::tuple tri_tuple = tri_item.cast<py::tuple>();
      if (tri_tuple.size() != 3)
      {
        throw std::runtime_error("Triangle tuple must have 3 elements (dr, dc, is_up).");
      }
      tris_cpp.emplace_back(tri_tuple[0].cast<int>(), tri_tuple[1].cast<int>(), tri_tuple[2].cast<bool>());
    }

    if (color_py.size() != 3)
    {
      throw std::runtime_error("Color tuple must have 3 elements (r, g, b).");
    }
    tg::ColorCpp color_cpp = {color_py[0].cast<int>(), color_py[1].cast<int>(), color_py[2].cast<int>()};

    return tg::ShapeCpp(std::move(tris_cpp), color_cpp, id_py);
  }
  catch (const py::error_already_set &e)
  {
    throw std::runtime_error(std::string("Error converting Python shape to C++: ") + e.what());
  }
  catch (const std::exception &e)
  {
    throw std::runtime_error(std::string("Error converting Python shape to C++: ") + e.what());
  }
}

PYBIND11_MODULE(trianglengin_cpp, m)
{
  m.doc() = "C++ core module for Trianglengin";

  py::class_<tg::GameStateCpp>(m, "GameStateCpp")
      .def(py::init([](const py::object &py_config, unsigned int seed)
                    {
                 tg::EnvConfigCpp cpp_config = python_to_cpp_env_config(py_config);
                 return std::make_unique<tg::GameStateCpp>(cpp_config, seed); }),
           py::arg("config"), py::arg("initial_seed"))
      .def("reset", &tg::GameStateCpp::reset)
      .def("step", &tg::GameStateCpp::step, py::arg("action"))
      .def("is_over", &tg::GameStateCpp::is_over)
      .def("get_score", &tg::GameStateCpp::get_score)
      .def("get_valid_actions", &tg::GameStateCpp::get_valid_actions, py::arg("force_recalculate") = false, py::return_value_policy::reference_internal)
      .def("get_current_step", &tg::GameStateCpp::get_current_step)
      .def("get_game_over_reason", &tg::GameStateCpp::get_game_over_reason)
      .def("get_shapes_cpp", [](const tg::GameStateCpp &gs)
           {
            py::list shapes_list;
            for(const auto& shape_opt : gs.get_shapes()) {
                shapes_list.append(cpp_shape_to_python(shape_opt));
            }
            return shapes_list; })
      .def("get_grid_occupied_flat", [](const tg::GameStateCpp &gs)
           {
            const auto& grid = gs.get_grid_data().get_occupied_grid();
            size_t rows = grid.size();
            size_t cols = (rows > 0) ? grid[0].size() : 0;
            py::array_t<bool> result({rows, cols});
            auto buf = result.request();
            bool *ptr = static_cast<bool *>(buf.ptr);
            // Manual copy for std::vector<bool>
            for (size_t r = 0; r < rows; ++r) {
                for (size_t c = 0; c < cols; ++c) {
                    ptr[r * cols + c] = grid[r][c];
                }
            }
            return result; })
      .def("get_grid_colors_flat", [](const tg::GameStateCpp &gs)
           {
            const auto& grid = gs.get_grid_data().get_color_id_grid();
            size_t rows = grid.size();
            size_t cols = (rows > 0) ? grid[0].size() : 0;
            py::array_t<int8_t> result({rows, cols});
            auto buf = result.request();
            int8_t *ptr = static_cast<int8_t *>(buf.ptr);
             // memcpy is fine for int8_t
             for (size_t r = 0; r < rows; ++r) {
                std::memcpy(ptr + r * cols, grid[r].data(), cols * sizeof(int8_t));
            }
            return result; })
      .def("get_grid_death_flat", [](const tg::GameStateCpp &gs)
           {
            const auto& grid = gs.get_grid_data().get_death_grid();
            size_t rows = grid.size();
            size_t cols = (rows > 0) ? grid[0].size() : 0;
            py::array_t<bool> result({rows, cols});
            auto buf = result.request();
            bool *ptr = static_cast<bool *>(buf.ptr);
            // Manual copy for std::vector<bool>
             for (size_t r = 0; r < rows; ++r) {
                for (size_t c = 0; c < cols; ++c) {
                    ptr[r * cols + c] = grid[r][c];
                }
            }
            return result; })
      .def("copy", &tg::GameStateCpp::copy)
      .def("debug_toggle_cell", &tg::GameStateCpp::debug_toggle_cell, py::arg("r"), py::arg("c"))
      // Add binding for debug_set_shapes
      .def("debug_set_shapes", [](tg::GameStateCpp &gs, const py::list &shapes_py)
           {
            std::vector<std::optional<tg::ShapeCpp>> shapes_cpp;
            shapes_cpp.reserve(shapes_py.size());
            for(const auto& shape_item_handle : shapes_py) {
                // Cast handle to object before passing to conversion function
                py::object shape_item = py::reinterpret_borrow<py::object>(shape_item_handle);
                shapes_cpp.push_back(python_to_cpp_shape(shape_item));
            }
            gs.debug_set_shapes(shapes_cpp); }, py::arg("new_shapes"), "Sets the shapes in the preview slots directly (for debugging/testing).");

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}