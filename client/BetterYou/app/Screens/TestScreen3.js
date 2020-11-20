import React from 'react';
import { Text, View, SafeAreaView, StyleSheet, Dimensions } from 'react-native';
import AppText from '../components/AppText';
import IconButton from '../components/IconButton';
import TextButton from '../components/TextButton';
import TitleText from '../components/TitleText';

function TestScreen3() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titletext}>
        <TitleText style={{fontSize: 40}}>Fitness Goals</TitleText>
        <AppText style={{fontSize: 20, top: '5%', width: Dimensions.get('window').width * .90}}>How many minutes of activity would you like to get per day?</AppText>
      </View>
      <View style={styles.exampletextbox} />
      <View style={styles.searchcontainer}>
        <TextButton
          name={"Save"}
          onPress={() => console.log("pressed")}
        />
      </View>
      
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#9df0fc',
    //alignItems: 'center',
    //justifyContent: 'center',
  },
  exampletextbox: {
    backgroundColor: '#fff',
    height: 50,
    margin: 10,
    marginHorizontal: 20,
    marginBottom: 50,
    borderRadius: 10,
  },
  searchcontainer: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    flex: 0.2,
  },
  titletext: {
    top: '3%',
    left: '5%',
    //width: Dimensions.get('window').width * .85,
    flex: 0.3,
  },
});

export default TestScreen3;