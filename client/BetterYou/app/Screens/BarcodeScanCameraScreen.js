import React, { useEffect, useState } from "react";

import { View, Text, Modal, StyleSheet } from "react-native";
import { Camera } from "expo-camera";
import { TouchableOpacity } from "react-native-gesture-handler";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import HeaderText from "../components/HeaderText";
import AppText from "../components/AppText";

function BarcodeScanCameraScreen() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [product, setProduct] = useState("");

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const handleBarCodeScanned = ({ type, data }) => {
    setScanned(true);
    // api call to get product
    const result = "Ground Beef";
    setProduct(result);

    setModalVisible(true);
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }
  return (
    <View style={{ flex: 1 }}>
      <Modal animationType="slide" transparent={true} visible={modalVisible}>
        <View
          style={{
            backgroundColor: "white",
            flex: 1,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <HeaderText style={{ marginBottom: 20 }}>{product}</HeaderText>
          <View
            style={{
              flexDirection: "row",
              justifyContent: "space-evenly",
              alignItems: "stretch",
              width: "100%",
            }}
          >
            <TouchableOpacity
              onPress={() => {
                setModalVisible(false);
                setScanned(false);
              }}
            >
              <AppText style={styles.linkText}>Scan again</AppText>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => {
                console.log("navigate to entry form screen");
              }}
            >
              <AppText style={styles.linkText}>Continue</AppText>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
      <Camera
        style={{ flex: 1 }}
        type={Camera.Constants.Type.back}
        autoFocus="on"
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
      >
        <View
          style={{
            flex: 1,
            justifyContent: "flex-end",
            backgroundColor: "transparent",
            paddingBottom: 40,
          }}
        >
          <View
            style={{
              flexDirection: "row",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <TouchableOpacity
              style={{ marginHorizontal: 30 }}
              onPress={() =>
                console.log("navigate back to input type selection screen")
              }
            >
              <MaterialCommunityIcons
                name="window-close"
                color="#fff"
                size={40}
              />
            </TouchableOpacity>
          </View>
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  linkText: {
    color: "#4da6cf",
  },
});

export default BarcodeScanCameraScreen;
