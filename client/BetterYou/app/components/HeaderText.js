import React from 'react';
import {StyleSheet, Text} from 'react-native';

function HeaderText({children, style}) {
    return (
        <Text style={[styles.text, style]}>{children}</Text>
    );
}

const styles = StyleSheet.create({
    text: {
        fontWeight: "bold",
        fontSize: 20
    }
})

export default HeaderText;