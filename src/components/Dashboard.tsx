import React from 'react';
import { Bell, Camera, Shield, UserCircle } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';

interface DashboardProps {
  activeAlerts: number;
  threatsDetected: number;
  systemStatus: string;
  cameras: Array<{ id: number; name: string; location: string; status: string }>;
}

const Dashboard: React.FC<DashboardProps> = ({ activeAlerts, threatsDetected, systemStatus, cameras }) => {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <header className="border-b border-slate-800 p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">SecureWatch AI</h1>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            <div className="flex items-center gap-2">
              <UserCircle className="h-6 w-6" />
              <span>المشرف</span>
            </div>
          </div>
        </div>
      </header>

      <div className="grid gap-6 p-6 md:grid-cols-3">
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-slate-400">التنبيهات النشطة</p>
              <h2 className="text-3xl font-bold">{activeAlerts}</h2>
            </div>
            <Bell className="h-8 w-8 text-blue-500" />
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-slate-400">التهديدات المكتشفة</p>
              <h2 className="text-3xl font-bold">{threatsDetected}</h2>
            </div>
            <Shield className="h-8 w-8 text-red-500" />
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-slate-400">حالة النظام</p>
              <h2 className="text-xl font-bold text-green-500">{systemStatus}</h2>
            </div>
            <div className="h-3 w-3 rounded-full bg-green-500"></div>
          </CardContent>
        </Card>
      </div>

      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">بث الكاميرات</h2>
          <Button className="bg-blue-500 hover:bg-blue-600">
            <Camera className="h-4 w-4 mr-2" />
            إضافة كاميرا
          </Button>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          {cameras.map((camera) => (
            <Card key={camera.id} className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="aspect-video bg-slate-900 relative">
                  <div className="absolute top-4 left-4 flex items-center gap-2">
                    <Camera className="h-5 w-5" />
                    <span>{camera.name}</span>
                  </div>
                  <div className="absolute top-4 right-4 flex items-center gap-2">
                    <div className={`h-2 w-2 rounded-full ${camera.status === 'active' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <span className="text-sm">{camera.status === 'active' ? 'مباشر' : 'غير متصل'}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

