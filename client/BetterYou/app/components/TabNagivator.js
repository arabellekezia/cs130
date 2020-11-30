import React from 'react';

import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
//import { AntDesign, Ionicons } from "@expo/vector-icons";


import TestScreen2 from '../Screens/TestScreen2';
import TestScreen3 from '../Screens/TestScreen3';


import StartScreen from '../Screens/StartScreen';

const Tab = createBottomTabNavigator();

function TabNagivator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Summary') {
            iconName = focused
              ? 'ios-stats'
              : 'ios-stats';
          } else if (route.name === 'New Entry') {
            iconName = focused ? 'ios-add-circle' : 'ios-add-circle-outline';
          } else if (route.name === 'Goals') {
            iconName = focused ? 'md-trending-up' : 'md-trending-up'
          }

          // You can return any component that you like here!
          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
      tabBarOptions={{
        activeTintColor: 'tomato',
        inactiveTintColor: 'gray',
      }}
    >
      <Tab.Screen name="Summary" component={StartScreen} />
      <Tab.Screen name="New Entry" component={TestScreen2} />
      <Tab.Screen name="Goals" component={TestScreen3} />
    </Tab.Navigator>
  );
}

export default TabNagivator;