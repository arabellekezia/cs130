import React from "react";

import { View, StyleSheet} from "react-native";
import AppText from "./AppText";
import Icon from "./Icon";

function SummaryItem({ name, size, iconColor = "black", detail, unit, label, secondaryDetail, secondaryUnit, style }) {
  return (
    <View style={{...styles.container, ...style}}>
      <Icon
        name={name}
        size={size}
        backgroundColor="white"
        iconColor={iconColor}
        iconScale={0.9}
      />
      <AppText>
        <AppText style={{ fontSize: 22, lineHeight: 34,  textAlign: "center"}}>{detail}</AppText>
        <AppText style={{ fontSize: 15}}>{` ${unit}`}</AppText>
        {secondaryDetail && <AppText style={{ fontSize: 22, lineHeight: 34,  textAlign: "center"}}>{` ${secondaryDetail}`}</AppText>}
        {secondaryUnit && <AppText style={{ fontSize: 15}}>{` ${secondaryUnit}`}</AppText>}
      </AppText>
      <AppText style={{ fontSize: 16,  textAlign: "center", width: 100, }}>{label}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    //justifyContent: "center",
    //justifyContent: "space-around",
    paddingVertical: 7,
    alignItems: "center",
  },
});

export default SummaryItem;
