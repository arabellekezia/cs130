import React from 'react';
import { StyleSheet, Text, View , SafeAreaView} from 'react-native';

import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import TestScreen1 from '../Screens/TestScreen1';
import TestScreen2 from '../Screens/TestScreen2';

const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={TestScreen1} />
        <Tab.Screen name="Settings" component={TestScreen2} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
  },
})

export default TabNavigator;