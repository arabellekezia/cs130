import { StatusBar } from "expo-status-bar";
import React, { useEffect } from "react";
import { StyleSheet, Text, View, SafeAreaView } from "react-native";

import Ionicons from "react-native-vector-icons/Ionicons";

import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import DemoScreen from "./app/components/DemoScreen";
import SummaryScreen from "./app/Screens/SummaryScreen";
import TestScreen2 from "./app/Screens/TestScreen2";
import TabNagivator from "./app/components/TabNagivator";
import LoginScreen from "./app/Screens/LoginScreen";
import WeeklyFitnessScreen from "./app/Screens/WeeklyFitnessScreen";
import DailyNutritionScreen from "./app/Screens/DailyNutritionScreen";
import DailySleepScreen from "./app/Screens/DailySleepScreen";
import WeeklySleepScreen from "./app/Screens/WeeklySleepScreen";
import DietGoalsScreen from "./app/Screens/DietGoalsScreen";
import SleepEntryFormScreen from "./app/Screens/SleepEntryFormScreen";
import FitnessGoalsScreen from "./app/Screens/FitnessGoalsScreen";
import FitnessGoalEntryTypeSelectScreen from "./app/Screens/FitnessGoalEntryTypeSelectScreen";
import DailyFitnessScreen from "./app/Screens/DailyFitnessScreen";
import WeeklyNutritionScreen from "./app/Screens/WeeklyNutritionScreen";
import SignupScreen from "./app/Screens/SignupScreen";
import AppNavigator from "./app/navigation/AppNavigator";
import navTheme from "./app/navigation/navTheme";
import AuthNavigator from "./app/navigation/AuthNavigator";
import { getUserToken } from "./app/utils/token";
import { AppLoading } from "expo";

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

export default function App() {
  // will need to be set by checking if auth token is inside asyncStorage. Make userToken as a state variable and effect hook to retrieve token on first load
  // https://reactnavigation.org/docs/auth-flow/#how-it-will-work

  const [isSignedIn, setIsSignedIn] = React.useState(false);
  const [isReady, setIsReady] = React.useState(false);

  async function fetchToken() {
    const userToken = await getUserToken();
    setIsSignedIn(userToken !== null);
  }

  if (!isReady) {
    return (
      <AppLoading
        startAsync={fetchToken}
        onFinish={() => setIsReady(true)}
        onError={console.warn}
      />
    );
  }
  return (
    <NavigationContainer theme={navTheme}>
      {isSignedIn ? <AppNavigator /> : <AuthNavigator />}
    </NavigationContainer>
  );
  // return <LoginScreen />
}


    // <WeeklyFitnessScreen />
    // <WeeklySleepScreen />
    // <WeeklyNutritionScreen />

    // <DailyFitnessScreen />
    // <DailySleepScreen />
    // <DailyNutritionScreen />

    // <DietGoalsScreen />
    //<SleepEntryFormScreen />
    //<FitnessGoalsScreen />
    // <FitnessGoalEntryTypeSelectScreen />

    // <DemoScreen />
    // <LoginScreen />
    // <SignupScreen />
    // <DemoScreen />
    // <SummaryScreen />

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
