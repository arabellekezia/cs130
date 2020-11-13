import React from "react";
import { View, useWindowDimensions, StyleSheet, Platform } from "react-native";

import { LineChart } from "react-native-chart-kit";

function AppLineChart({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  backgroundColor = "#ffffff",
  bezier,
  scaleDimensions = 1,
  yAxisSuffix = "",
}) {
  return (
    <View>
      <LineChart
        data={data}
        width={scaleDimensions * useWindowDimensions().width}
        height={scaleDimensions * 200}
        yAxisSuffix={yAxisSuffix}
        chartConfig={{
          backgroundColor: backgroundColor,
          backgroundGradientFrom: backgroundColor,
          backgroundGradientTo: backgroundColor,
          decimalPlaces: 0,
          color: color,
          labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          propsForDots: {
            r: "5",
            strokeWidth: "2",
            stroke: backgroundColor,
          },
        }}
        bezier={bezier}
        style={styles.container}
      />
    </View>
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

export default AppLineChart;
