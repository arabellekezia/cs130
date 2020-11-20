import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View , SafeAreaView} from 'react-native';

import Ionicons from 'react-native-vector-icons/Ionicons';

import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import DemoScreen from './app/components/DemoScreen';
import TestScreen1 from './app/Screens/TestScreen1';
import TestScreen2 from './app/Screens/TestScreen2';



const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      {/*<Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === 'Summary') {
              iconName = focused
                ? 'ios-information-circle'
                : 'ios-information-circle-outline';
            } else if (route.name === 'Settings') {
              iconName = focused ? 'ios-list-box' : 'ios-list';
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
        <Tab.Screen name="Summary" component={TestScreen1} />
        <Tab.Screen name="Settings" component={TestScreen2} />
      </Tab.Navigator>*/}
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={TestScreen1} />
        <Stack.Screen name="Details" component={TestScreen2} />
      </Stack.Navigator>
    </NavigationContainer>
      
    /* <DemoScreen /> 

    <Text>Open up App.js to start working on your app!</Text> 
    StatusBar style="auto" /> */
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
