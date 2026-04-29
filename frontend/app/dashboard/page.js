'use client';
import { useEffect, useState } from 'react';
import API from '../../lib/api';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState('');
  const [selectedProject, setSelectedProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { router.push('/login'); return; }
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    const res = await API.get('/projects/');
    setProjects(res.data);
  };

  const fetchTasks = async (projectId) => {
    const res = await API.get(`/tasks/project/${projectId}`);
    setTasks(res.data);
    setSelectedProject(projectId);
  };

  const createProject = async () => {
    if (!newProject.trim()) return;
    await API.post('/projects/', { name: newProject });
    setNewProject('');
    fetchProjects();
  };

  const createTask = async () => {
    if (!newTask.trim() || !selectedProject) return;
    await API.post('/tasks/', { title: newTask, project_id: selectedProject });
    setNewTask('');
    fetchTasks(selectedProject);
  };

  const updateTaskStatus = async (taskId, status) => {
    await API.put(`/tasks/${taskId}`, { status });
    fetchTasks(selectedProject);
  };

  const deleteProject = async (projectId) => {
    await API.delete(`/projects/${projectId}`);
    setSelectedProject(null);
    setTasks([]);
    fetchProjects();
  };

  const logout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <button onClick={logout} className="text-sm text-red-500 hover:underline">Logout</button>
        </div>

        {/* Projects Section */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Projects</h2>
          <div className="flex gap-2 mb-4">
            <input value={newProject} onChange={e => setNewProject(e.target.value)}
              placeholder="New project name"
              className="border rounded-lg px-4 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <button onClick={createProject} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {projects.map(p => (
              <div key={p.id} className={`flex items-center gap-2 px-4 py-2 rounded-full border cursor-pointer transition
                ${selectedProject === p.id ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 hover:border-blue-400'}`}>
                <span onClick={() => fetchTasks(p.id)}>{p.name}</span>
                <button onClick={() => deleteProject(p.id)} className="text-xs hover:text-red-400 ml-1">✕</button>
              </div>
            ))}
          </div>
        </div>

        {/* Tasks Section */}
        {selectedProject && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-4">Tasks</h2>
            <div className="flex gap-2 mb-4">
              <input value={newTask} onChange={e => setNewTask(e.target.value)}
                placeholder="New task title"
                className="border rounded-lg px-4 py-2 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              <button onClick={createTask} className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                Add Task
              </button>
            </div>

            {/* Task columns */}
            <div className="grid grid-cols-3 gap-4">
              {['todo', 'in_progress', 'done'].map(status => (
                <div key={status} className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-600 mb-3 capitalize">{status.replace('_', ' ')}</h3>
                  {tasks.filter(t => t.status === status).map(task => (
                    <div key={task.id} className="bg-white border rounded-lg p-3 mb-2 shadow-sm">
                      <p className="text-sm text-gray-700 mb-2">{task.title}</p>
                      <select value={task.status} onChange={e => updateTaskStatus(task.id, e.target.value)}
                        className="text-xs border rounded px-2 py-1 w-full">
                        <option value="todo">Todo</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                      </select>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}