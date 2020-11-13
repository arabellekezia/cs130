import React from "react";
import { View, StyleSheet, TouchableOpacity } from "react-native";
import AppText from "./AppText";
import Icon from "./Icon";

function IconButton({ name, size, iconColor = "black", label, onPress }) {
  return (
    <TouchableOpacity onPress={onPress}>
      <View style={styles.container}>
        <Icon
          name={name}
          size={size}
          backgroundColor="white"
          iconColor={iconColor}
          iconScale={0.6}
          border
        />
        <AppText style={{ fontSize: size * 0.25, marginTop: size * 0.125 }}>
          {label}
        </AppText>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "center",
  },
});

export default IconButton;
