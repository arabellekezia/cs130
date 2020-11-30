import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import EntryCategorySelectScreen from "../Screens/EntryCategorySelectScreen";
import GoalSelectionScreen from "../Screens/GoalSelectionScreen";
import StartScreen from "../Screens/StartScreen";

import { MaterialCommunityIcons } from "@expo/vector-icons";

const Tab = createBottomTabNavigator();

function AppNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Summary"
        component={StartScreen}
        options={{
          tabBarIcon: ({ size, color }) => (
            <MaterialCommunityIcons
              name="chart-line"
              size={size}
              color={color}
            />
          ),
        }}
      />
      <Tab.Screen
        name="New Entry"
        component={EntryCategorySelectScreen}
        options={{
          tabBarIcon: ({ size, color }) => (
            <MaterialCommunityIcons
              name="plus-circle"
              size={size}
              color={color}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Goals"
        component={GoalSelectionScreen}
        options={{
          tabBarIcon: ({ size, color }) => (
            <MaterialCommunityIcons
              name="flag-triangle"
              size={size}
              color={color}
            />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export default AppNavigator;
