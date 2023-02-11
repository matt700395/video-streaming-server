import React from 'react';
import { View, StyleSheet } from 'react-native';
import VideoStream from './VideoStream';

const App = () => {
  return (
    <View style={styles.container}>
      <VideoStream />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default App;
