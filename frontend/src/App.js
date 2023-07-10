import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Component for displaying nested JSON data with formatting
function JSONDisplay({ data, level = 0 }) {
  const createMarkup = (data) => {
    let markup = [];

    const applyFormatting = (text, level) => {
      const colors = ["#b0b0b0", "#d0d0d0", "#e0e0e0", "#f0f0f0"];
      const backgroundColor = colors[level % colors.length];

      if (level < 1) {
        return <strong style={{ backgroundColor }}>{text}</strong>;
      } else if (level % 2 === 0) {
        return <em style={{ backgroundColor }}>{text}</em>;
      } else {
        return <span style={{ backgroundColor }}>{text}</span>;
      }
    };

    if (Array.isArray(data)) {
      data.forEach((value, index) => {
        if (typeof value === 'object' && value !== null) {
          markup.push(
            <div key={index} style={{ paddingLeft: `${level * 20}px` }}>
              {applyFormatting(`${index}:`, level)}
              <JSONDisplay data={value} level={level + 1} />
            </div>
          );
        } else {
          markup.push(
            <div key={index} style={{ paddingLeft: `${level * 20}px` }}>
              {applyFormatting(`${index}:`, level)} {value}
            </div>
          );
        }
      });
    } else {
      Object.keys(data).forEach((key, index) => {
        const value = data[key];
        if (typeof value === 'object' && value !== null) {
          markup.push(
            <div key={index} style={{ paddingLeft: `${level * 20}px` }}>
              {applyFormatting(`${key}:`, level)}
              <JSONDisplay data={value} level={level + 1} />
            </div>
          );
        } else {
          markup.push(
            <div key={index} style={{ paddingLeft: `${level * 20}px` }}>
              {applyFormatting(`${key}:`, level)} {value}
            </div>
          );
        }
      });
    }
    return markup;
  };

  return <div>{createMarkup(data)}</div>;
}

// Main App component
function App() {
  // Define state variables
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Pre-defined loading messages
  const messages = ["Finding a pipette...", "Growing cells...", "Running PCR...", "Engineering new lifeforms...", "Sequencing DNA...", /* ...more messages... */];

  // Handle loading message updates
  useEffect(() => {
    let messageIndex = 0;
    let intervalId = null;

    // If loading, start a loop to update the loading message every 10 seconds
    if (isLoading) {
      intervalId = setInterval(() => {
        setLoadingMessage(messages[messageIndex % messages.length]);
        messageIndex += 1;
      }, 10000);
    }

    // Cleanup function to clear the interval when loading ends
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isLoading]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setIsSubmitted(true);

    try {
      // Send a POST request to the backend
      const response = await axios.post('/api/main', { input: input });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      // Stop loading and reset isSubmitted state
      setIsLoading(false);
      setIsSubmitted(false);
    }
  };

  // Render the component
  return (
    <div className="App">
      <h1 className="App-title">molbio.ai</h1>
      <h2 className="App-version-title">1.0.0</h2>
      <header className="App-header">
        <form onSubmit={handleSubmit}>
          <input className="App-input" type="text" value={input} onChange={e => setInput(e.target.value)} />
          <button className="App-button" type="submit">{isSubmitted ? 'Submitted' : 'Plan out your bio research project, start-to-finish, step-by-step, in under 30 seconds'}</button>
        </form>

        {isLoading && <div>{loadingMessage}</div>}

        {!isLoading && result && <JSONDisplay data={result} />}

      </header>
    </div>
  );
}

export default App;
