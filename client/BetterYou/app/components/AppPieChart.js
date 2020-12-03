import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { PieChart } from "react-native-chart-kit";

function AppPieChart({
  data,
  accessor,
  paddingLeft,
  absolute,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  backgroundColor = "transparent",
  scaleDimensions = 1,
}) {
  console.log(data);
  return (
    <PieChart
      data={data}
      accessor={accessor}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      bgColor={backgroundColor}
      paddingLeft={paddingLeft}
      absolute={absolute}
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        color: color,
        labelColor: labelColor,
      }}
      style={styles.container}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
    ...Platform.select({
      ios: {
        // // styles for box shadow
        // shadowOpacity: 0.1,
        // shadowRadius: 5,
        // shadowColor: "#000",
        // shadowOffset: { height: 1, width: 1 },
      },
      android: {
        // android styles
      },
    }),
  },
});

export default AppPieChart;
