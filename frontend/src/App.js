import React, { useState } from 'react';
import { Upload, Loader2 } from 'lucide-react';

const App = () => {
  const [inputs, setInputs] = useState([
    { type: 'file', value: null },
    { type: 'file', value: null },
    { type: 'file', value: null }
  ]);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const toggleMode = (index) => {
    const newInputs = [...inputs];
    newInputs[index] = { 
      type: newInputs[index].type === 'file' ? 'text' : 'file', 
      value: null 
    };
    setInputs(newInputs);
  };

  const handleInputChange = (index, val) => {
    const newInputs = [...inputs];
    newInputs[index].value = val;
    setInputs(newInputs);
  };

  const runAnalysis = async () => {
    setLoading(true);
    const formData = new FormData();
    inputs.forEach((input, i) => {
      if (input.value) {
        if (input.type === 'file') {
          formData.append(`file${i + 1}`, input.value);
        } else {
          const blob = new Blob([input.value], { type: 'text/plain' });
          formData.append(`file${i + 1}`, blob, `textinput${i+1}.txt`);
        }
      }
    });
    try {
      const res = await fetch('http://localhost:5000/analyze', { method: 'POST', body: formData });
      const result = await res.json();
      setData(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = async () => {
    const formData = new FormData();
    inputs.forEach((input, i) => {
      if (input.value) {
        if (input.type === 'file') {
          formData.append(`file${i + 1}`, input.value);
        } else {
          const blob = new Blob([input.value], { type: 'text/plain' });
          formData.append(`file${i + 1}`, blob, `textinput${i+1}.txt`);
        }
      }
    });
    const res = await fetch('http://localhost:5000/export', { method: 'POST', body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'emr_results.csv';
    a.click();
  };

  return (
    <div className="min-h-screen bg-[#D9EAE8] flex flex-col items-center py-12 px-4">
      <h1 className="text-4xl font-semibold text-gray-800 mb-2">EMR Data Parser</h1>
      <p className="text-gray-600 mb-12">Upload files or paste text to analyze...</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12 w-full max-w-5xl">
        {inputs.map((input, i) => (
          <div key={i} className="flex flex-col gap-4">
            <div className="bg-[#AAB7D1] rounded-[24px] h-64 flex flex-col items-center justify-center overflow-hidden">
              {input.type === 'file' ? (
                <label className="cursor-pointer flex flex-col items-center justify-center w-full h-full">
                  <Upload size={64} className="mb-4 text-gray-800" />
                  <span className="text-gray-800 font-medium px-4 text-center">
                    {input.value ? input.value.name : "Upload File..."}
                  </span>
                  <input type="file" className="hidden" onChange={(e) => handleInputChange(i, e.target.files[0])} />
                </label>
              ) : (
                <textarea
                  className="w-full h-full bg-transparent p-4 text-gray-800 placeholder-gray-600 outline-none resize-none"
                  placeholder="Paste clinical notes here..."
                  onChange={(e) => handleInputChange(i, e.target.value)}
                />
              )}
            </div>
            <button onClick={() => toggleMode(i)} className="bg-[#D1D1D1] py-2 px-6 rounded-lg text-sm font-medium">
              {input.type === 'file' ? "Switch to Text Input" : "Switch to File Upload"}
            </button>
          </div>
        ))}
      </div>
      <button onClick={runAnalysis} disabled={loading} className="bg-[#AAB7D1] px-16 py-4 rounded-[20px] text-2xl font-medium text-gray-800 flex items-center gap-3">
        {loading ? <Loader2 className="animate-spin" /> : "Analyze Data..."}
      </button>
      {data && (
        <div className="mt-12 w-full max-w-4xl bg-white rounded-xl p-6 shadow-lg">
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(data).map(([key, val]) => (
              <div key={key} className="border-b pb-2">
                <span className="font-semibold text-gray-600 uppercase text-xs">{key}:</span> <span className="text-blue-600 ml-2">{val}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      {data && (
        <button
          onClick={downloadCSV}
          className="mt-6 bg-[#4CAF50] text-white px-12 py-3 rounded-[20px] text-xl font-medium"
        >
          Download CSV
        </button>
      )}
    </div>
  );
};

export default App;