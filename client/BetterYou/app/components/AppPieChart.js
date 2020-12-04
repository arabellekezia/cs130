import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { PieChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize PieChart from react-native-chart-kit in our other components much more easily.
 * @module
 * @param { Object } ParameterObj The Object that encompasses all the parameters
 * @param { Object } ParameterObj.data Data that is accepted by PieChart to process
 * @param { string } ParameterObj.accessor Property in the data object from which the number values are taken
 * @param { string } ParameterObj.paddingLeft padding on the left of the chart
 * @param { boolean } ParameterObj.absolute true = real values on pie chart legend, false = percentages
 * @param { Function => string } [ParameterObj.color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the pie slices
 * @param { Function => string } [ParameterObj.labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { string } [ParameterObj.backgroundColor = "#ffffff"] Sets background color of chart
 * @param { number } [ParameterObj.scaleDimensions = 1] Number with which to scale the chart size
 * @returns {PieChart} A PieChart with the following paramters added and consistent configuration for the whole application
 */
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
  //console.log(data);
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
