import React, { useEffect, useState } from 'react';
import Dashboard from '../components/Dashboard';

const DashboardPage: React.FC = () => {
  const [dashboardData, setDashboardData] = useState({
    activeAlerts: 0,
    threatsDetected: 0,
    systemStatus: '',
    cameras: [],
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('/api/dashboard/');
        if (response.ok) {
          const data = await response.json();
          setDashboardData(data);
        } else {
          throw new Error('Failed to fetch dashboard data');
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    fetchDashboardData();
  }, []);

  return <Dashboard {...dashboardData} />;
};

export default DashboardPage;

