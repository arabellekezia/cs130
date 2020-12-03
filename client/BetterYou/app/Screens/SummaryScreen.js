import React from "react";
import { SafeAreaView, StyleSheet, View, Dimensions } from "react-native";

import ListItemComponent from "../components/ListItemComponent";
import Icon from "../components/Icon";
import AppBarChart from "../components/AppBarChart";
import TitleText from "../components/TitleText";
import { ScrollView } from "react-native-gesture-handler";
import AppText from "../components/AppText";
import FitnessService from "../services/FitnessService";
import colors from "../config/colors";

import DateUtils from "../utils/date";
import { useIsFocused } from "@react-navigation/native";

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


function getFitnessCardData(weeklyEntries) {
  const dayOfWeekLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const activeTimeData = {
    labels: dayOfWeekLabels,
    datasets: [{ data: [], strokeWidth: 2 }],
  };
  let totalActiveTime = 0;
  weeklyEntries.forEach((entry) => {
    totalActiveTime += entry.activeTime;
    activeTimeData.datasets[0].data.push(entry.activeTime.toFixed(0));
  });
  return {
    activeTimeData,
    averageActiveTime: (totalActiveTime / 7).toFixed(0),
  };
}

function getFitnessDailySummary(dailyEntries) {
  let totalActiveTime = 0;
  dailyEntries.forEach((entry) => {
    totalActiveTime += entry.Minutes;
  });
  return totalActiveTime.toFixed(1);
}

function SummaryScreen({ navigation }) {
  const currentDay = DateUtils.getFormattedDate();
  const [isReady, setIsReady] = React.useState(false);
  const [fitnessCardData, setFitnessCardData] = React.useState(false);
  const [fitnessDailySummary, setFitnessDailySummary] = React.useState(false);
  const isFocused = useIsFocused();

  React.useEffect(() => {
    async function fetchFitnessData() {
      const [weeklyEntries, dailyEntries] = await Promise.all([
        FitnessService.getWeeklyFitnessEntries(),
        FitnessService.getDailyFitnessEntries(),
      ]);
      setFitnessCardData(getFitnessCardData(weeklyEntries));
      setFitnessDailySummary(getFitnessDailySummary(dailyEntries));
      setIsReady(true);
    }
    fetchFitnessData();
  }, [isFocused]);

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
                iconColor={colors.sleep}
                iconScale={0.85}
                border={0}
              />
            }
            description="7 hours slept"
            containerStyle={{ borderColor: colors.sleep }}
            titleStyle={{ color: colors.sleep }}
            onPress={() => navigation.navigate("DailySleep")}
          />

          <ListItemComponent
            title="Nutrition"
            icon={
              <Icon
                name="food-apple"
                size={17}
                backgroundColor="white"
                iconColor={colors.diet}
                iconScale={1}
              />
            }
            description="1850 calories"
            containerStyle={{ borderColor: colors.diet }}
            titleStyle={{ color: colors.diet }}
            onPress={() => navigation.navigate("DailyNutrition")}
          />

          {isReady && <ListItemComponent
            title="Fitness"
            icon={
              <Icon
                name="google-fit"
                size={17}
                backgroundColor="white"
                iconColor={colors.fitness}
                iconScale={1}
              />
            }
            description={`${fitnessDailySummary} minutes of active time`}
            containerStyle={{ borderColor: colors.fitness }}
            titleStyle={{ color: colors.fitness }}
            onPress={() => navigation.navigate("DailyFitness")}
          />}
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
            containerStyle={{ borderColor: colors.sleep }}
            titleStyle={{ color: colors.sleep }}
            onPress={() => navigation.navigate("WeeklySleep")}
          >
            <View style={styles.chartcontainer}>
              <View style={styles.charts}>
                <AppBarChart
                  data={data}
                  color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
                  scaleDimensions={0.8}
                />
              </View>
            </View>
          </ListItemComponent>
        </View>

        <View style={styles.listItems}>
          <ListItemComponent
            style={styles.graphCard}
            title="Nutrition"
            description={
              <AppText>
                You consumed an average of
                <AppText style={styles.boldText} children={` 2000 calories `} />
                per day over the last 7 days.
              </AppText>
            }
            containerStyle={{ borderColor: colors.diet }}
            titleStyle={{ color: colors.diet }}
            onPress={() => navigation.navigate("WeeklyNutrition")}
          >
            <View style={styles.chartcontainer}>
              <View style={styles.charts}>
                <AppBarChart
                  data={data}
                  color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
                  scaleDimensions={0.8}
                />
              </View>
            </View>
          </ListItemComponent>
        </View>

        {isReady && (
          <View style={styles.listItems}>
            <ListItemComponent
              style={styles.graphCard}
              title="Fitness"
              description={
                <AppText>
                  You've exercised for an average of
                  <AppText
                    style={styles.boldText}
                    children={` ${fitnessCardData.averageActiveTime} minutes `}
                  />
                  per day over the last 7 days.
                </AppText>
              }
              containerStyle={{ borderColor: colors.fitness }}
              titleStyle={{ color: colors.fitness }}
              onPress={() => navigation.navigate("WeeklyFitness")}
            >
              <View style={styles.chartcontainer}>
                <View style={styles.charts}>
                  <AppBarChart
                    data={fitnessCardData.activeTimeData}
                    color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
                    scaleDimensions={0.8}
                  />
                </View>
              </View>
            </ListItemComponent>
          </View>
        )}
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
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 8,
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
    marginBottom: 30,
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
