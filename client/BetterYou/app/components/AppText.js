import React from 'react';

import { StyleSheet, Text } from 'react-native';

function AppText({children, style, testID}) {
    return (
        <Text style={[styles.text, style]} testID={testID}>{children}</Text>
    );
}

const styles = StyleSheet.create({
    text: {
    }
})

export default AppText;