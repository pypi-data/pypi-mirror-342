// File: src/trianglengin/cpp/config.h
#ifndef TRIANGLENGIN_CPP_CONFIG_H
#define TRIANGLENGIN_CPP_CONFIG_H

#pragma once

#include <vector>
#include <tuple>
#include <cstdint>

namespace trianglengin::cpp
{
  struct EnvConfigCpp
  {
    int rows = 8;
    int cols = 15;
    std::vector<std::tuple<int, int>> playable_range_per_row = {
        {3, 12}, {2, 13}, {1, 14}, {0, 15}, {0, 15}, {1, 14}, {2, 13}, {3, 12}};
    int num_shape_slots = 3;
    double reward_per_placed_triangle = 0.01;
    double reward_per_cleared_triangle = 0.5;
    double reward_per_step_alive = 0.005;
    double penalty_game_over = -10.0;
    int action_dim = 0;
  };
} // namespace trianglengin::cpp

#endif // TRIANGLENGIN_CPP_CONFIG_H