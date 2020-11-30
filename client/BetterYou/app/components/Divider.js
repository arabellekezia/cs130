import React from "react";

import { View, StyleSheet } from "react-native";

function Divider({ height }) {
  return <View style={[styles.divider, { height: height }]}></View>;
}

const styles = StyleSheet.create({
  divider: {
    backgroundColor: "black",
    width: "100%",
    marginVertical: 5,
  },
});
export default Divider;
