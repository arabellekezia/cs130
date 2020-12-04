import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { ProgressChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize ProgressRing from react-native-chart-kit in our other components much more easily.
 * @module
 * @param { Object } ParameterObj The Object that encompasses all the parameters
 * @param { Object } ParameterObj.data Data that is accepted by ProgressRing to process
 * @param { Function => string } [ParameterObj.color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the rings
 * @param { Function => string } [ParameterObj.labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { number } [ParameterObj.strokeWidth = 16] Thickness of the ring
 * @param { number } [ParameterObj.radius = 32] Radius of the ring
 * @param { string } [ParameterObj.backgroundColor = "#ffffff"] Sets background color of chart
 * @param { number } [ParameterObj.scaleDimensions = 1] Number with which to scale the chart size
 * @param { boolean } ParameterObj.hideLegend True = hide the legend, False = keep legend
 * @returns {ProgressRing} A ProgressRing with the following paramters added and consistent configuration for the whole application
 */
function AppProgressRing({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  strokeWidth = 16,
  radius = 32,
  backgroundColor = "#ffffff",
  scaleDimensions = 1,
  hideLegend,
}) {
  return (
    <ProgressChart
      data={data}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      strokeWidth={strokeWidth}
      radius={radius}
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        color: color,
        labelColor: labelColor,
      }}
      style={styles.container}
      hideLegend={hideLegend}
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

export default AppProgressRing;
