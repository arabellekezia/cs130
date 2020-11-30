import React from "react";

import { createStackNavigator } from "@react-navigation/stack";
import GoalSelectionScreen from "../Screens/GoalSelectionScreen";
import DietGoalsScreen from "../Screens/DietGoalsScreen";
import FitnessGoalsScreen from "../Screens/FitnessGoalsScreen";
import SleepGoalsScreen from "../Screens/SleepGoalsScreen";

const Stack = createStackNavigator();
function GoalsNavigator(props) {
  return (
    <Stack.Navigator>
      <Stack.Screen name="GoalSelection" component={GoalSelectionScreen} />
      <Stack.Screen name="DietGoals" component={DietGoalsScreen} />
      <Stack.Screen name="FitnessGoals" component={FitnessGoalsScreen} />
      <Stack.Screen name="SleepGoals" component={SleepGoalsScreen} />
    </Stack.Navigator>
  );
}

export default GoalsNavigator;
