import React, { useEffect } from "react";
import { StyleSheet } from "react-native";

import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import AppNavigator from "./app/navigation/AppNavigator";
import navTheme from "./app/navigation/navTheme";
import AuthNavigator from "./app/navigation/AuthNavigator";
import AuthContext from "./app/context/AuthContext";
import { getUserToken } from "./app/utils/token";
import { AppLoading } from "expo";

import { LogBox } from 'react-native';

LogBox.ignoreLogs(['Warning: ...']);
LogBox.ignoreAllLogs();

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

export default function App() {
  // will need to be set by checking if auth token is inside asyncStorage. Make userToken as a state variable and effect hook to retrieve token on first load
  // https://reactnavigation.org/docs/auth-flow/#how-it-will-work

  const [isSignedIn, setIsSignedIn] = React.useState(false);
  const [isReady, setIsReady] = React.useState(false);

  async function fetchToken() {
    try {
      const userToken = await getUserToken();
      setIsSignedIn(userToken !== null);
    } catch (err) {
      console.log(err);
    }
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
    <AuthContext.Provider value={{ isSignedIn, setIsSignedIn }}>
      <NavigationContainer theme={navTheme}>
        {isSignedIn ? <AppNavigator /> : <AuthNavigator />}
      </NavigationContainer>
    </AuthContext.Provider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
