import React from "react";
import Icon from "./Icon";
import { StyleSheet, View } from "react-native";
import AppText from "./AppText";

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
          size={24}
          iconScale={0.9}
        />
        <AppText style={styles.startTime} children={startTime} />
      </View>
      <AppText style={styles.activity} children={activity} />
      <View style={styles.rowContainer}>
        <AppText
          style={styles.stats}
          children={`${duration} · ${caloriesBurned} Cal`}
        />
        <Icon
          name="fire"
          backgroundColor="white"
          iconColor="grey"
          size={22}
          iconScale={0.9}
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
    marginLeft: 4,
    marginTop: 3,
    marginBottom: 4,
  },
  stats: {
    marginLeft: 4,
    fontSize: 16,
  },
});

export default FitnessEntry;
