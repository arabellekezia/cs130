import React from "react";

import { createStackNavigator } from "@react-navigation/stack";
import GoalSelectionScreen from "../Screens/GoalSelectionScreen";
import DietGoalsScreen from "../Screens/DietGoalsScreen";
import FitnessGoalsScreen from "../Screens/FitnessGoalsScreen";
import SleepGoalsScreen from "../Screens/SleepGoalsScreen";
import colors from "../config/colors";

const Stack = createStackNavigator();
function GoalsNavigator(props) {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: colors.white,
        },
      }}
    >
      <Stack.Screen
        name="GoalSelection"
        component={GoalSelectionScreen}
        options={{ title: "Goals" }}
      />
      <Stack.Screen
        name="DietGoals"
        component={DietGoalsScreen}
        options={{ title: "Diet Goals" }}
      />
      <Stack.Screen
        name="FitnessGoals"
        component={FitnessGoalsScreen}
        options={{ title: "Fitness Goals" }}
      />
      <Stack.Screen
        name="SleepGoals"
        component={SleepGoalsScreen}
        options={{ title: "Sleep Goals" }}
      />
    </Stack.Navigator>
  );
}

export default GoalsNavigator;
