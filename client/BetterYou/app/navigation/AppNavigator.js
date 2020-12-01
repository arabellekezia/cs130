import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import EntryCategorySelectScreen from "../Screens/EntryCategorySelectScreen";
import GoalSelectionScreen from "../Screens/GoalSelectionScreen";

import { MaterialCommunityIcons } from "@expo/vector-icons";
import NewEntryNavigator from "./NewEntryNavigator";
import GoalsNavigator from "./GoalsNavigator";
import SummaryScreen from "../Screens/SummaryScreen";

const Tab = createBottomTabNavigator();

function AppNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Summary"
        component={SummaryScreen}
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
        component={NewEntryNavigator}
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
        component={GoalsNavigator}
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
