import React from "react";
import { SafeAreaView, StyleSheet, View, Dimensions } from "react-native";

import ListItemComponent from "../components/ListItemComponent";
import Icon from "../components/Icon";
import AppBarChart from "../components/AppBarChart";
import TitleText from "../components/TitleText";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";

import moment from "moment";

const data = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      data: [6.5, 4, 6, 5, 7, 6, 8],
      strokeWidth: 2, // optional
    },
  ],
  legend: ["Hours Slept"], // optional
};

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("dddd, MMMM Do");
}

function SummaryScreen({ navigation }) {
  const currentDay = getToday();
  return (
    <SafeAreaView>
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle}>Daily Summary</TitleText>
        <AppText style={styles.dateHeader} children={currentDay} />
        <View style={styles.listItems}>
          <ListItemComponent
            title="Sleep"
            icon={
              <Icon
                name="sleep"
                size={17}
                backgroundColor="white"
                iconColor="black"
                iconScale={0.85}
                border={0}
              />
            }
            description="7 hours slept"
            onPress={() => navigation.navigate("DailySleep")}
          />

          <ListItemComponent
            title="Nutrition"
            icon={
              <Icon
                name="food-apple"
                size={17}
                backgroundColor="white"
                iconColor="black"
                iconScale={1}
              />
            }
            description="1850 Calories"
            onPress={() => navigation.navigate("DailyNutrition")}
          />

          <ListItemComponent
            title="Workout"
            icon={
              <Icon
                name="google-fit"
                size={17}
                backgroundColor="white"
                iconColor="black"
                iconScale={1}
              />
            }
            description="0.72 hours total active time"
            onPress={() => navigation.navigate("DailyFitness")}
          />
        </View>

        <TitleText style={styles.weeklyStatsHeader}>
          Weekly Statistics
        </TitleText>
        <View style={styles.listItems}>
          <ListItemComponent
            style={styles.graphCard}
            title="Sleep"
            description={
              <AppText>
                You averaged
                <AppText style={styles.boldText} children={` 6.07 hours `} />
                of sleep per day over the last 7 days.
              </AppText>
            }
            onPress={() => navigation.navigate("WeeklySleep")}
          >
            <View style={styles.chartcontainer}>
              <View style={styles.charts}>
                <AppBarChart
                  data={data}
                  color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
                  scaleDimensions={0.8}
                />
              </View>
            </View>
          </ListItemComponent>
        </View>

        <View style={styles.listItems}>
          <ListItemComponent
            style={styles.graphCard}
            title="Diet"
            description={
              <AppText>
                You consumed an average of
                <AppText style={styles.boldText} children={` 2000 calories `} />
                per day over the last 7 days.
              </AppText>
            }
            onPress={() => navigation.navigate("WeeklyNutrition")}
          >
            <View style={styles.chartcontainer}>
              <View style={styles.charts}>
                <AppBarChart
                  data={data}
                  color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
                  scaleDimensions={0.8}
                />
              </View>
            </View>
          </ListItemComponent>
        </View>

        <View style={styles.listItems}>
          <ListItemComponent
            style={styles.graphCard}
            title="Fitness"
            description={
              <AppText>
                You exercised for an average of
                <AppText
                  style={styles.boldText}
                  children={` 120 active minutes `}
                />
                per day over the last 7 days.
              </AppText>
            }
            onPress={() => navigation.navigate("WeeklyFitness")}
          >
            <View style={styles.chartcontainer}>
              <View style={styles.charts}>
                <AppBarChart
                  data={data}
                  color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
                  scaleDimensions={0.8}
                />
              </View>
            </View>
          </ListItemComponent>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  boldText: {
    fontWeight: "bold",
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "15%",
    marginLeft: "5%",
    marginBottom: 6,
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
    marginBottom: "10%",
  },
  weeklyStatsHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 24,
    marginBottom: 24,
  },
  categoryHeaders: {
    fontSize: 24,
  },
  chartContainer: {
    alignItems: "center",
  },
  charts: {
    width: Dimensions.get("window").width * 0.5,
    marginRight: 150,
  },
  container: {
    alignItems: "center",
    justifyContent: "center",
  },
  listItems: {
    marginRight: "5%",
    marginBottom: 24,
  },
  graphCard: {
    marginRight: "20%",
    backgroundColor: "grey",
  },
});

export default SummaryScreen;
