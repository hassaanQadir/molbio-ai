import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  // Define state variables
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState(""); 
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Pre-defined loading messages
  const messages = ["Finding a pipette...", "Growing cells...", "Running PCR...", "Engineering new lifeforms...", "Sequencing DNA...", "Splicing genes...", "Preparing CRISPR...", "Optimizing BioBricks...", "Calibrating nanobots...", "Synthesizing proteins...", "Designing genetic circuits...", "Programming cells...", "Building biomolecules...", "Assembling genome...", "Loading Bioinformatics...", "Analyzing genetic data...", "Optimizing metabolic pathways...", "Performing gene therapy...", "Incubating bacteriophages...", "Initiating DNA replication...", "Running genetic algorithms...", "Formulating synthetic ecosystems...", "Generating synthetic life...", "Autoclaving lab equipment...", "Calibrating spectrophotometer...", "Culturing bacteria...", "Setting up microfluidic devices...", "Adjusting microbial fuel cells...", "Decoding genetic code...", "Setting up gene drive...", "Establishing microbiomes...", "Harvesting bioplastics...", "Fabricating BioMEMS..."];

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
      const response = await axios.post('/api/reverse', { input: input });
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
      <h2 className="App-version-title">0.9.0</h2>
      <header className="App-header">
      <form onSubmit={handleSubmit}>
      <input className="App-input" type="text" value={input} onChange={e => setInput(e.target.value)} />
      <button className="App-button" type="submit">{isSubmitted ? 'Submitted' : 'Outline and automate your bio research project now (Results return in ~30 minutes)'}</button>
      </form>

      {isLoading && <div>{loadingMessage}</div>}
      {!isLoading && result && <pre>{result}</pre>}
      </header>
    </div>
  );
}

export default App;
