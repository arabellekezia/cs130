import React from 'react';
import { SafeAreaView, StyleSheet, View, Dimensions } from 'react-native';

import ListItemComponent from '../components/ListItemComponent';
import Icon from '../components/Icon';
import AppLineChart from "../components/AppLineChart";
import AppBarChart from "../components/AppBarChart";
import AppProgressRing from "../components/AppProgressRing";
import AppStackedBarChart from "../components/AppStackedBarChart";
import TitleText from '../components/TitleText';
import { ScrollView } from 'react-native-gesture-handler';
import AppText from '../components/AppText';

const data = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      data: [6.5, 4, 6, 5, 7, 6, 8],
      // color: (opacity = 1) => `rgba(0, 0, 255, ${opacity})`, // optional
      strokeWidth: 2, // optional
    },
    // {
    //   data: [5, 4, 3, 3, 8, 4, 5],
    //   // color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`, // optional
    //   strokeWidth: 2, // optional
    // },
  ],
  legend: ["Hours Slept"], // optional
};

function TestScreen1( {navigation} ) {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <TitleText style={styles.titletexts}>Daily Summary</TitleText>
        <AppText>Friday, November 20th 2020</AppText>
        <View style={styles.listitems}>
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
            description="1850 Calories"
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
            description="0.72 hours total active time"
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
            description="7 hours slept"
          />
        </View>
        

        <TitleText>Weekly Statistics</TitleText>
        <View style={styles.chartcontainer}>
          <View style={styles.charts}>
            <TitleText style={{fontSize: 20, top: 5, left: 10}}>Sleep</TitleText>
            <AppText style={{ top: 5, left: 5, margin: 5}}>You averaged 6.07 hours of sleep over the last 7 days.</AppText>
            <AppBarChart
              data={data}
              color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
              scaleDimensions={0.85}
            />
          </View>
          <View style={styles.charts}>
            <TitleText style={{fontSize: 20, top: 5, left: 10}}>Diet</TitleText>
            <AppText style={{top: 5, left: 5, margin: 5}}>You consumed an average of 2000 calories per day over the last 7 days.</AppText>
            <AppBarChart
              data={data}
              color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
              scaleDimensions={0.85}
            />
          </View>
        </View>
        
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  chartcontainer: {
    //width: Dimensions.get('window').width * .85,
    alignItems: "center",
    //backgroundColor: '#fff',
  },
  charts:{
    width: Dimensions.get('window').width * .85,
    //alignItems: "center",
    backgroundColor: '#fff',
    //padding: 7,
    margin: 5,
    borderRadius: 10,
  },
  container: {
    flex: 1,
    backgroundColor: '#9df0fc',
    alignItems: 'center',
    justifyContent: 'center',
  },
  listitems: {
    alignItems: "center"
  },
  titletexts: {
    alignItems: "flex-start"
  }
});

export default TestScreen1;