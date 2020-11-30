import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import EntryCategorySelectScreen from "../Screens/EntryCategorySelectScreen";

import DietGoalEntryTypeSelectScreen from "../Screens/DietGoalEntryTypeSelectScreen";
import FitnessGoalEntryTypeSelectScreen from "../Screens/FitnessGoalEntryTypeSelectScreen";
import SleepGoalEntryTypeSelectScreen from "../Screens/SleepGoalEntryTypeScreen";
import FitnessTimerScreen from "../Screens/FitnessTimerScreen";
import SleepTimerScreen from "../Screens/SleepTimerScreen";
import SleepEntryFormScreen from "../Screens/SleepEntryFormScreen";
import FitnessEntryFormScreen from "../Screens/FitnessEntryFormScreen";
import FoodDatabaseSearchScreen from "../Screens/FoodDatabaseSearchScreen";
import FoodEntryFormScreen from "../Screens/FoodEntryFormScreen";
import BarcodeScanCameraScreen from "../Screens/BarcodeScanCameraScreen";
import colors from "../config/colors";

const Stack = createStackNavigator();

function NewEntryNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: colors.background,
        },
      }}
    >
      <Stack.Screen
        name="EntryCategorySelect"
        component={EntryCategorySelectScreen}
        options={{
          title: "New Entry",
        }}
      />
      <Stack.Screen
        name="DietGoalEntryTypeSelect"
        component={DietGoalEntryTypeSelectScreen}
        options={{
          title: "Input Method",
        }}
      />

      <Stack.Screen
        name="FitnessGoalEntryTypeSelect"
        component={FitnessGoalEntryTypeSelectScreen}
        options={{
          title: "Input Method",
        }}
      />
      <Stack.Screen
        name="SleepGoalEntryTypeSelect"
        component={SleepGoalEntryTypeSelectScreen}
        options={{
          title: "Input Method",
        }}
      />

      <Stack.Screen
        name="FitnessTimer"
        component={FitnessTimerScreen}
        options={{ title: "Workout Timer" }}
      />
      <Stack.Screen
        name="SleepTimer"
        component={SleepTimerScreen}
        options={{ title: "Sleep Timer" }}
      />

      <Stack.Screen
        name="SleepEntryForm"
        component={SleepEntryFormScreen}
        options={{ title: "Sleep Entry" }}
      />

      <Stack.Screen
        name="FitnessEntryForm"
        component={FitnessEntryFormScreen}
        options={{ title: "Fitness Entry" }}
      />
      <Stack.Screen
        name="FoodDatabaseSearch"
        component={FoodDatabaseSearchScreen}
        options={{ title: "Look up" }}
      />
      <Stack.Screen
        name="FoodEntryForm"
        component={FoodEntryFormScreen}
        options={{ title: "Food Entry" }}
      />
      <Stack.Screen
        name="BarcodeScanCamera"
        component={BarcodeScanCameraScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

export default NewEntryNavigator;
