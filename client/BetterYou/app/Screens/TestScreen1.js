import React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';

import ListItemComponent from '../components/ListItemComponent';
import Icon from '../components/Icon';

function TestScreen1( {navigation} ) {
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
        //navigation= {navigation.navigate("Details")}
        destination="Details"
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

export default TestScreen1;