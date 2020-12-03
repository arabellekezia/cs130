import React from "react";

import { createStackNavigator } from "@react-navigation/stack";
import SummaryScreen from "../Screens/SummaryScreen";
import DailyFitnessScreen from "../Screens/DailyFitnessScreen";
import DailyNutritionScreen from "../Screens/DailyNutritionScreen";
import DailySleepScreen from "../Screens/DailySleepScreen";
import WeeklyFitnessScreen from "../Screens/WeeklyFitnessScreen";
import WeeklyNutritionScreen from "../Screens/WeeklyNutritionScreen";
import WeeklySleepScreen from "../Screens/WeeklySleepScreen";
import { Button } from "react-native";
import Icon from "../components/Icon";
import IconButton from "../components/IconButton";
import { TouchableOpacity } from "react-native-gesture-handler";
import { clearUserToken } from "../utils/token"


const Stack = createStackNavigator();

function SummaryNavigator(props) {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Summary" component={SummaryScreen} 
        options={{
          headerRight: () => (
            <TouchableOpacity onPress={async () => {await clearUserToken()}} activeOpacity={0.7}>
              <Icon
                name="logout"
                size={50}
                backgroundColor="white"
                iconColor="grey"
              />
            </TouchableOpacity>
          ),
        }}
      />
      <Stack.Screen
        name="DailyFitness"
        component={DailyFitnessScreen}
        options={{ title: "Daily Fitness" }}
      />
      <Stack.Screen
        name="DailyNutrition"
        component={DailyNutritionScreen}
        options={{ title: "Daily Nutrition" }}
      />
      <Stack.Screen
        name="DailySleep"
        component={DailySleepScreen}
        options={{ title: "Daily Sleep" }}
      />
      <Stack.Screen
        name="WeeklyFitness"
        component={WeeklyFitnessScreen}
        options={{ title: "Weekly Fitness" }}
      />
      <Stack.Screen
        name="WeeklyNutrition"
        component={WeeklyNutritionScreen}
        options={{ title: "Weekly Nutrition" }}
      />
      <Stack.Screen
        name="WeeklySleep"
        component={WeeklySleepScreen}
        options={{ title: "Weekly Sleep" }}
      />
    </Stack.Navigator>
  );
}

export default SummaryNavigator;
