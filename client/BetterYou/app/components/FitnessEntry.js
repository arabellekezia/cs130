import React from "react";
import Icon from "./Icon";
import { StyleSheet, View } from "react-native";
import AppText from "./AppText";


/**
 * This function produces a visual component that organizes and displays a single Fitness Entry in a visually appealing way
 * @param {StyleSheet} style Possible Additional stylesheet (optional)
 * @param {string} iconName name of the MaterialCommunityIcons icon that will be fed into the Icon component
 * @param {string} startTime string formatted from moment().format() that denotes start time of the activity
 * @param {string} activity name of the activity; this corresponds to the category in the backend
 * @param {string} duration string formatted from moment().duration().format() that denotes the duration of the activity
 * @param {number} caloriesBurned number of calories burnt from the activity
 * @returns {View} A View that contains everything to be displayed with the parameters filling in the details
 */
function FitnessEntry({
  style,
  iconName,
  startTime,
  activity,
  duration,
  caloriesBurned,
}) {
  return (
    <View style={{ ...styles.container, ...style }}>
      <View style={styles.rowContainer}>
        <Icon
          name={iconName}
          backgroundColor="white"
          iconColor="grey"
          size={21}
          iconScale={1}
        />
        <AppText style={styles.startTime} children={startTime} />
      </View>
      <AppText style={styles.activity} children={activity} />
      <View style={styles.rowContainer}>
        <AppText
          style={styles.stats}
          children={`${duration} · ${caloriesBurned} kcal`}
        />
        <Icon
          name="fire"
          backgroundColor="white"
          iconColor="grey"
          size={18}
          iconScale={1}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "flex-start",
  },
  rowContainer: {
    flexDirection: "row",
    justifyContent: "flex-start",
    alignItems: "center",
  },
  startTime: {
    fontSize: 16,
    marginLeft: 4,
  },
  activity: {
    fontWeight: "bold",
    fontSize: 18,
    marginLeft: 5,
    marginTop: 3,
    marginBottom: 4,
  },
  stats: {
    marginLeft: 5,
    fontSize: 16,
  },
});

export default FitnessEntry;
