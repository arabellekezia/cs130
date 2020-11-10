import React from 'react';
import {StyleSheet, Text} from 'react-native';

function TitleText({children, style}) {
    return (
        <Text style={[styles.text, style]}>{children}</Text>
    );
}

const styles = StyleSheet.create({
    text: {
        fontWeight: "bold",
        fontSize: 30
    }
})

export default TitleText;