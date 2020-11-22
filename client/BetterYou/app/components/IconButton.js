import React from "react";
import { View, StyleSheet, TouchableOpacity } from "react-native";
import AppText from "./AppText";
import Icon from "./Icon";

function IconButton({
  name,
  size,
  iconColor = "black",
  backgroundColor = "white",
  textColor = "#474747",
  label,
  onPress,
  border = 0,
  style,
}) {
  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      <View style={{ ...styles.container, ...style }}>
        <Icon
          name={name}
          size={size}
          backgroundColor={backgroundColor}
          iconColor={iconColor}
          iconScale={0.6}
          border={border}
        />
        <AppText
          style={{
            fontSize: size * 0.25,
            marginTop: size * 0.125,
            color: textColor,
          }}
        >
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
