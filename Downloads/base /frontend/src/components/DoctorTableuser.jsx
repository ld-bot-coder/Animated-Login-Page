import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import { FaDownload } from 'react-icons/fa';
import { FiRefreshCw } from 'react-icons/fi';
import { IoIosOptions } from 'react-icons/io';
import { FaChartLine } from 'react-icons/fa';
import { saveAs } from 'file-saver'; // Import file-saver for downloading CSV

const DoctorTableuser = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [userRole, setUserRole] = useState(''); // State for user role
  const recordsPerPage = 10;

  useEffect(() => {
    fetchData(); // Fetch data on component mount
    fetchUserRoleFromLocalStorage(); // Fetch user role from local storage on component mount
  }, []);

  const fetchData = () => {
    axios.get('http://localhost:3004/api/auth/doctors')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  };
console.log(data)
  const fetchUserRoleFromLocalStorage = () => {
    const role = localStorage.getItem('role'); // Get user role from local storage
    if (role) {
      setUserRole(role);
    } else {
      console.error('No user role found in local storage');
    }
  };

  const downloadCSV = () => {
    const csvContent = data.map(row => [
      row.reocrd_id,
      row.name,
      row.bcngnf ? 'Yes' : 'No',
      row.Email,
      row.phone,
      row.Specialization,
      row.rcountry,
      row.rstate,
      row.Address
    ]).map(e => e.join(",")).join("\n");

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'doctors.csv');
  };

  const lastIndex = currentPage * recordsPerPage;
  const firstIndex = lastIndex - recordsPerPage;
  const currentRecords = data.slice(firstIndex, lastIndex);
  const totalPages = Math.ceil(data.length / recordsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handlePageClick = (page) => {
    setCurrentPage(page);
  };

  const getPageNumbers = () => {
    const pageNumbers = [];
    const maxPagesToShow = 3;
    const leftSide = Math.max(1, currentPage - 1);
    const rightSide = Math.min(totalPages, currentPage + 1);

    if (totalPages <= maxPagesToShow + 2) {
      for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
      }
    } else {
      if (currentPage > maxPagesToShow) {
        pageNumbers.push(1);
        pageNumbers.push('...');
      }

      for (let i = leftSide; i <= rightSide; i++) {
        pageNumbers.push(i);
      }

      if (currentPage < totalPages - maxPagesToShow) {
        pageNumbers.push('...');
        pageNumbers.push(totalPages);
      }
    }

    return pageNumbers;
  };

  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-4 md:p-6 bg-white-100">
        <style>
          {`
            .truncated-address {
              display: block;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
              max-width: 100%;
            }
            
            .full-address {
              display: none;
            }
            
            .address-container:hover .truncated-address {
              display: none;
            }
            
            .address-container:hover .full-address {
              display: block;
              white-space: normal; /* Allow wrapping of the full address */
            }
          `}
        </style>
        <div className="mb-4 md:mb-6">
          <div className="mb-4">
            <h2 className="text-lg md:text-xl font-semibold mb-1" style={{ color: '#7C3783' }}>
              Find Your Pediatricians
            </h2>
            <p className="text-gray-400 text-xs">
              Filter based on location and subspeciality
            </p>
          </div>
          <div className="flex flex-col md:flex-row items-center justify-between mb-4">
            <div className="text-gray-700 text-xs mb-2 md:mb-0">Showing {currentRecords.length} results out of {data.length}</div>
            <div className="flex items-center space-x-4 mr-5">
              <button><IoIosOptions /></button>
              {userRole !== 'client' && (
                <button
                  className="p-2 bg-white rounded-full shadow hover:bg-gray-100 transition text-xs"
                  onClick={downloadCSV}
                >
                  <FaDownload className="text-gray-600 text-xs" />
                </button>
              )}
              <button
                className="p-2 bg-white rounded-full shadow hover:bg-gray-100 transition text-xs"
                onClick={fetchData}
              >
                <FiRefreshCw />
              </button>
              <p className='text-xs'>chart view</p>
              <button><FaChartLine /></button>
            </div>
          </div>
          <div className="overflow-x-auto">
  <table className="min-w-full bg-white border border-gray-300 rounded-lg shadow-md table-fixed">
    <thead>
      <tr>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Name</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Email</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Email2</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Phone</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Phone2</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Specialty</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">City</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">State</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal">Pincode</th>
        <th className="p-2 md:p-3 text-left border-b text-xs font-normal" style={{ width: '20%' }}>Address</th>
      </tr>
    </thead>
    <tbody>
      {currentRecords.map((Doctor, index) => (
        <tr key={index}>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Name}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Email}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Email2}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Phone}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Phone2}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Specialty}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.City}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.State}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">{Doctor.Pincode}</td>
          <td className="p-2 md:p-3 border-b text-xs text-gray-500">
            <div className="address-container relative">
              <span className="truncated-address">
                {Doctor.Address.length > 14 ? `${Doctor.Address.substring(0, 14)}...` : Doctor.Address}
              </span>
              <span className="full-address">{Doctor.Address}</span>
            </div>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
        </div>
        <div className="flex items-center justify-between mt-4">
          <button
            className="p-2 bg-white rounded-full shadow hover:bg-gray-100 transition text-xs"
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
          >
            Prev
          </button>
          <div className="text-xs">
            {getPageNumbers().map((pageNumber, index) => (
              <button
                key={index}
                className={`px-3 py-1 ${pageNumber === currentPage ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'} rounded-full mx-1`}
                onClick={() => pageNumber !== '...' && handlePageClick(pageNumber)}
              >
                {pageNumber}
              </button>
            ))}
          </div>
          <button
            className="p-2 bg-white rounded-full shadow hover:bg-gray-100 transition text-xs"
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default DoctorTableuser;
