// File: src/trianglengin/cpp/shape_logic.h
#ifndef TRIANGLENGIN_CPP_SHAPE_LOGIC_H
#define TRIANGLENGIN_CPP_SHAPE_LOGIC_H

#pragma once

#include <vector>
#include <random>
#include <optional>

#include "structs.h" // Needs ShapeCpp definition

namespace trianglengin::cpp
{

  // Forward declare GameStateCpp as it's used in function signatures
  class GameStateCpp;

  namespace shape_logic
  {
    std::vector<ShapeCpp> load_shape_templates();

    void refill_shape_slots(GameStateCpp &game_state, std::mt19937 &rng);

  } // namespace shape_logic
} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_SHAPE_LOGIC_H