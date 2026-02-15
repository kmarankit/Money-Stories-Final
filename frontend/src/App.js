import React, { useState, useEffect,useMemo } from 'react';
import api from './services/api';
import { 
  ChevronDown, ChevronUp, FileText, Github, 
  AlertTriangle, List, Upload, Download 
} from 'lucide-react';
import './App.css';
import * as pdfjsLib from "pdfjs-dist";
import { GlobalWorkerOptions } from "pdfjs-dist";

GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;




// --- SUB-COMPONENT: SideInfoDropdowns ---
const SideInfoDropdowns = () => {
  const [openIndex, setOpenIndex] = useState(0);
  const items = [
    { title: 'Assignment Question', icon: <List size={18}/>, content: 'Automate the extraction of P&L, Balance Sheet, and Cash Flow statements from complex multi-page financial PDFs using AI Vision.' },
    { title: 'Project Limitations', icon: <AlertTriangle size={18}/>, content: 'Maximum file size is 20MB. AI parsing credits are limited. Accuracy depends on the scan quality.' },
    { title: 'Described Answer', icon: <FileText size={18}/>, content: 'Frontend:-React.js,Tailwind CSS,Flowbite | Backend:-Python, FastAPI, Uvicorn,python-dotenv,Gemini 2.5 Flash, LlamaParse,Camelot ' },
    { title: 'GitHub Link', icon: <Github size={18}/>, content: <a href="https://github.com/kmarankit/Money-Stories-Final/" target="_blank" rel="noreferrer" className="green-link">View Repository</a> },
  ];
  const handleDownloadDocumentation = () => {
    const link = document.createElement('a');
    link.href = '/Money Stories.pdf'; // Ensure this file is in your public folder
    link.setAttribute('download', 'Money Stories by ankit kumar.pdf');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="side-dropdowns">
      {items.map((item, idx) => (
        <div key={idx} className={`dropdown-item ${openIndex === idx ? 'open' : ''}`}>
          <div className="dropdown-header" onClick={() => setOpenIndex(openIndex === idx ? -1 : idx)}>
            <div className="header-left">{item.icon} <span>{item.title}</span></div>
            {openIndex === idx ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>
          {openIndex === idx && <div className="dropdown-body">{item.content}</div>}
        </div>
      ))}
<button className='btn-primary' onClick={handleDownloadDocumentation}>
        Download Project Documentation
      </button>
      
    </div>
  );
};

// --- SUB-COMPONENT: SidebarProfile ---
const SidebarProfile = () => (
  <div className="sidebar-profile-card">
    <div className="sidebar-profile-inner">
      <img src="/PHOTO.jpg" alt="Ankit Kumar" className="sidebar-avatar" />
      <div className="sidebar-info-text">
        <h4 className="profile-name-text">Ankit Kumar</h4>
        <p className="profile-detail">+91-7903335271</p>
        <p className="profile-detail">ak373714@gmail.com</p>
      </div>
    </div>
  </div>
   
);


// --- MAIN COMPONENT: App ---
const App = () => {
  const [setSelectedSample] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentLog, setCurrentLog] = useState("");
  const [data, setData] = useState({ pnl: [], balanceSheet: [], cashFlow: [], others: [] });
  const [excelBuffer, setExcelBuffer] = useState(null);
  
  // Rotating Log Messages for User Engagement
const loadingLogs = useMemo(() => [
  "Uploading PDF to Secure Server...",
  "LlamaParse: Initializing AI Vision Engine...",
  "Analyzing Document Structure...",
  "Locating Financial Tables...",
  "Gemini: Mapping Line Items to Schema...",
  "Cleaning Numerical Data...",
  "Finalizing Yearly Calculations...",
  "Generating Formatted Excel Sheet..."
], []);


  // Logic to handle Progress Bar and Logs
  useEffect(() => {
    let progInterval;
    let logInterval;
    let logIndex = 0;

    if (loading) {
      // Progress behavior: fast to 70%, slow to 95%, then waits
      progInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev < 70) return prev + 5;
          if (prev < 95) return prev + 1;
          return prev; // Stay at 95% until backend finishes
        });
      }, 800);

      // Log behavior: Rotate one line at a time
      setCurrentLog(loadingLogs[0]);
      logInterval = setInterval(() => {
        logIndex = (logIndex + 1) % loadingLogs.length;
        setCurrentLog(loadingLogs[logIndex]);
      }, 3000);
    } else {
      setProgress(0);
      setCurrentLog("");
    }

    return () => {
      clearInterval(progInterval);
      clearInterval(logInterval);
    };
  }, [loading,loadingLogs]);

 const handleFileChange = async (e) => {
  const f = e.target.files[0];
  if (!f) return;

  try {
    const fileReader = new FileReader();

    fileReader.onload = async function () {
      const typedArray = new Uint8Array(this.result);

      const pdf = await pdfjsLib.getDocument({ data: typedArray }).promise;
      const totalPages = pdf.numPages;

      if (totalPages > 10) {
        alert("❌ PDF exceeds 10 pages. Please upload a file with 10 pages or fewer.");
        return;
      }

      setSelectedSample(null);
      setFile(f);
    };

    fileReader.readAsArrayBuffer(f);

  } catch (error) {
    console.error("PDF validation error:", error);
    alert("Invalid PDF file.");
  }
};


  const handleProcess = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/api/upload', formData);
      if (response.data.success) {
        let extracted = response.data.financialData;
        
        // Safety: Flatten data if returned as nested table objects
        const formatTable = (tbl) => (tbl && tbl[0]?.rows ? tbl.flatMap(t => t.rows) : tbl || []);
        
        setData({
          pnl: formatTable(extracted.pnl),
          balanceSheet: formatTable(extracted.balanceSheet),
          cashFlow: formatTable(extracted.cashFlow),
          others: formatTable(extracted.others)
        });
        setExcelBuffer(response.data.excelBuffer);
        setProgress(100);
      }
    } catch (err) {
      console.error("Extraction error:", err);
      alert("Extraction failed. Please check the backend console.");
    } finally {
      setTimeout(() => setLoading(false), 1000);
    }
  };

  const downloadExcel = () => {
    if (!excelBuffer) return;
    const byteCharacters = atob(excelBuffer);
    const byteNumbers = new Array(byteCharacters.length).fill(0).map((_, i) => byteCharacters.charCodeAt(i));
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = `Financial_Report_${Date.now()}.xlsx`;
    link.click();
  };

  return (
    <div className="dashboard">
      <header className="navbar">
        <div className="nav-inner">
          <h2>Money Stories Finserv Dashboard</h2>
          <img src="/PHOTO.jpg" alt="User" className="nav-avatar" />
        </div>
      </header>

      <main className="main-content">
        <div className="dashboard-grid">
          <div className="info-side">
            <SideInfoDropdowns />
            <SidebarProfile />
          </div>

          <div className="upload-side">
            <section className="upload-card">
              <h3>Upload Financial PDF</h3>
              <div className="upload-area-container">
                <input id="fInput" type="file" onChange={handleFileChange} accept=".pdf" style={{ display: 'none' }} />
                <div className="upload-dropzone" onClick={() => document.getElementById('fInput').click()}>
                  <Upload size={40} color="#2e7d32" />
                  <div className="drop-text">
                    <strong>{file ? file.name : "Click to upload Financial PDF"}</strong>
                  </div>
                </div>
                <div className="process-actions">
                  <button onClick={handleProcess} disabled={loading || !file} className="btn-primary">
                    {loading ? "Processing..." : "Extract Data"}
                  </button>
                </div>
              </div>

              {loading && (
                <div className="progress-section">
                  <div className="progress-container">
                    <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                  </div>
                  {/* Dynamic background log */}
                  <p className="loading-log-text">{currentLog}</p>
                </div>
              )}
            </section>

            {data.pnl.length > 0 && (
              <section className="result-card">
                <div className="result-header">
                  <h3>Extracted Yearly Results</h3>
                  <button onClick={downloadExcel} className="btn-success"><Download size={16}/> Download Excel</button>
                </div>
                <div className="table-wrapper">
                  <table className="data-table">
                    <thead>
                      <tr>
                        {Object.keys(data.pnl[0]).map(k => <th key={k}>{k.replace(/_/g, ' ')}</th>)}
                      </tr>
                    </thead>
                    <tbody>
                      {data.pnl.map((row, i) => (
                        <tr key={i}>
                          {Object.values(row).map((val, j) => (
                            <td key={j}>
                              {/* Fix: Check if value is an object before rendering */}
                              {typeof val === 'object' && val !== null 
                                ? JSON.stringify(val) 
                                : (val?.toString() || "-")}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;