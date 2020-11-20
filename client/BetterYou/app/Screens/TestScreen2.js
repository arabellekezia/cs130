import React from 'react';
import { Text, View, SafeAreaView, StyleSheet, Dimensions } from 'react-native';
import IconButton from '../components/IconButton';
import TitleText from '../components/TitleText';

function TestScreen2() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titletext}>
        <TitleText style={{fontSize: 40}}>New Diet Entry</TitleText>
      </View>
      
      <View style={styles.searchcontainer}>
        <IconButton 
          name="barcode-scan"
          size={70}
          iconColor="black"
          label="Scan Barcode"
          fontSize={10}
          onPress={() => console.log("icon pressed")}
        />
        <IconButton 
          name="feature-search-outline"
          size={70}
          iconColor="black"
          label="Search"
          fontSize={10}
          onPress={() => console.log("icon pressed")}
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
  searchcontainer: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    flex: 1,
  },
  titletext: {
    top: '3%', 
    left: '5%',
    flex: 0.2,
  },
});

export default TestScreen2;