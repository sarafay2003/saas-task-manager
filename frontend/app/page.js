import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Task Manager</h1>
      <p className="text-gray-500 mb-8">Manage your projects and tasks efficiently</p>
      <div className="flex gap-4">
        <Link href="/login" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
          Login
        </Link>
        <Link href="/register" className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300">
          Register
        </Link>
      </div>
    </main>
  );
}