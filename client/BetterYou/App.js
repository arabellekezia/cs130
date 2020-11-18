import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View , SafeAreaView} from 'react-native';

import DemoScreen from './app/components/DemoScreen';
import ListItemComponent from './app/components/ListItemComponent';
import Icon from './app/components/Icon';
import TabNavigator from './app/components/TabNavigator';

import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

var iconexample = <Icon
name="food-variant"
size={30}
backgroundColor="white"
iconColor="black"
iconScale={1}
/>

function HomeScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Home!</Text>
    </View>
  );
}

function SettingsScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Settings!</Text>
    </View>
  );
}

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <ListItemComponent
        title="Nutrition"
        icon={<Icon
          name="food-variant"
          size={30}
          backgroundColor="white"
          iconColor="black"
          iconScale={0.80}
          border = {1}
          />}
        description="Touch for Nutrition Data"
      />

      <ListItemComponent
        title="Workout"
        icon={<Icon
          name="dumbbell"
          size={30}
          backgroundColor="white"
          iconColor="black"
          iconScale={0.85}
          border = {1}
          />}
        description="Touch for Workout Data"
      />

      <ListItemComponent
        title="Sleep"
        icon={<Icon
          name="sleep"
          size={30}
          backgroundColor="white"
          iconColor="black"
          iconScale={0.8}
          border = {1}
          />}
        description="Touch for Sleep Data"
        />
      <TabNavigator />
      
      {/* <DemoScreen /> 

      <Text>Open up App.js to start working on your app!</Text> */}
      <StatusBar style="auto" /> 
    </SafeAreaView>
    
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
