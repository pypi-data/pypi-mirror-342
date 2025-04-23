// File: src/trianglengin/cpp/shape_logic.cpp
#include "shape_logic.h"
#include "game_state.h" // Include full definition for implementation
#include <stdexcept>
#include <algorithm>

namespace trianglengin::cpp::shape_logic
{
  // --- Shape Templates (Keep as defined previously) ---
  const std::vector<std::vector<TriangleData>> PREDEFINED_SHAPE_TEMPLATES_CPP = {
      {{0, 0, true}},
      {{0, 0, true}},
      {{0, 0, true}, {1, 0, false}},
      {{0, 0, true}, {1, 0, false}},
      {{0, 0, false}},
      {{0, 0, true}, {0, 1, false}},
      {{0, 0, true}, {0, 1, false}},
      {{0, 0, false}, {0, 1, true}},
      {{0, 0, false}, {0, 1, true}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}},
      {{0, 0, false}, {0, 1, true}, {0, 2, false}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}, {1, 0, false}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}, {1, 2, false}},
      {{0, 0, false}, {0, 1, true}, {1, 0, true}, {1, 1, false}},
      {{0, 0, true}, {0, 2, true}, {1, 0, false}, {1, 1, true}, {1, 2, false}},
      {{0, 0, true}, {1, -2, false}, {1, -1, true}, {1, 0, false}},
      {{0, 0, true}, {0, 1, false}, {1, 0, false}, {1, 1, true}},
      {{0, 0, true}, {0, 1, false}, {1, 0, false}, {1, 1, true}, {1, 2, false}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}, {1, 0, false}, {1, 1, true}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}, {1, 0, false}, {1, 2, false}},
      {{0, 0, true}, {0, 1, false}, {0, 2, true}, {1, 1, true}, {1, 2, false}},
      {{0, 0, true}, {0, 2, true}, {1, 0, false}, {1, 1, true}, {1, 2, false}},
      {{0, 0, true}, {0, 1, false}, {1, 0, false}, {1, 1, true}, {1, 2, false}},
      {{0, 0, false}, {0, 1, true}, {1, 1, false}},
      {{0, 0, true}, {1, -1, true}, {1, 0, false}},
      {{0, 0, true}, {1, 0, false}, {1, 1, true}},
      {{0, 0, true}, {1, -1, true}, {1, 0, false}, {1, 1, true}},
      {{0, 0, true}, {1, -1, true}, {1, 0, false}},
      {{0, 0, false}, {0, 1, true}, {0, 2, false}, {1, 1, false}},
      {{0, 0, false}, {0, 1, true}, {1, 1, false}},
      {{0, 0, true}, {0, 1, false}, {1, 0, false}},
  };

  const std::vector<ColorCpp> SHAPE_COLORS_CPP = {
      {220, 40, 40}, {60, 60, 220}, {40, 200, 40}, {230, 230, 40}, {240, 150, 20}, {140, 40, 140}, {40, 200, 200}, {200, 100, 180}, {100, 180, 200}};
  const std::vector<int> SHAPE_COLOR_IDS_CPP = {0, 1, 2, 3, 4, 5, 6, 7, 8};

} // namespace trianglengin::cpp::shape_logic

namespace trianglengin::cpp::shape_logic
{

  ShapeCpp generate_random_shape(
      std::mt19937 &rng,
      const std::vector<ColorCpp> &available_colors,
      const std::vector<int> &available_color_ids)
  {
    if (PREDEFINED_SHAPE_TEMPLATES_CPP.empty() || available_colors.empty() || available_colors.size() != available_color_ids.size())
    {
      throw std::runtime_error("Shape templates or colors are not properly initialized.");
    }

    std::uniform_int_distribution<size_t> template_dist(0, PREDEFINED_SHAPE_TEMPLATES_CPP.size() - 1);
    size_t template_index = template_dist(rng);
    const auto &chosen_template = PREDEFINED_SHAPE_TEMPLATES_CPP[template_index];

    std::uniform_int_distribution<size_t> color_dist(0, available_colors.size() - 1);
    size_t color_index = color_dist(rng);
    const auto &chosen_color = available_colors[color_index];
    int chosen_color_id = available_color_ids[color_index];

    return ShapeCpp(chosen_template, chosen_color, chosen_color_id);
  }

  void refill_shape_slots(GameStateCpp &game_state, std::mt19937 &rng)
  {
    bool needs_refill = true;
    // Use the public getter to access shapes
    for (const auto &shape_opt : game_state.get_shapes())
    {
      if (shape_opt.has_value())
      {
        needs_refill = false;
        break;
      }
    }

    if (!needs_refill)
      return;

    // Use the mutable getter to modify shapes
    auto &shapes_ref = game_state.get_shapes_mut();
    for (size_t i = 0; i < shapes_ref.size(); ++i)
    {
      shapes_ref[i] = generate_random_shape(rng, SHAPE_COLORS_CPP, SHAPE_COLOR_IDS_CPP);
    }
    game_state.invalidate_action_cache();
  }

} // namespace trianglengin::cpp::shape_logic