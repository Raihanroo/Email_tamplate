<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

/**
 * Email Automation API Service for Laravel
 * 
 * This service integrates with Django Email Automation System
 * Base URL: http://127.0.0.1:8000/api/
 */
class EmailAutomationService
{
    private $baseUrl = 'http://127.0.0.1:8000/api';

    /**
     * Get all students
     * 
     * @return array
     */
    public function getAllStudents()
    {
        $response = Http::get("{$this->baseUrl}/students/");
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to fetch students: ' . $response->body());
    }

    /**
     * Upload Excel file with student data
     * 
     * @param string $filePath Path to Excel file
     * @param bool $replaceAll Delete existing data before upload
     * @return array
     */
    public function uploadExcel($filePath, $replaceAll = false)
    {
        $response = Http::attach(
            'file', 
            file_get_contents($filePath), 
            basename($filePath)
        )->post("{$this->baseUrl}/upload/", [
            'replace_all' => $replaceAll ? 'true' : 'false'
        ]);
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to upload Excel: ' . $response->body());
    }

    /**
     * Add a single student
     * 
     * @param array $studentData
     * @return array
     */
    public function addStudent(array $studentData)
    {
        $response = Http::post("{$this->baseUrl}/add-student/", $studentData);
        
        if ($response->successful()) {
            return $response->json();
        }
        
        // Check if duplicate email
        if ($response->status() === 400) {
            $error = $response->json();
            if (isset($error['error']) && strpos($error['error'], 'already exists') !== false) {
                throw new \Exception('Duplicate email: ' . $studentData['email']);
            }
        }
        
        throw new \Exception('Failed to add student: ' . $response->body());
    }

    /**
     * Update existing student by email
     * 
     * @param string $email
     * @param array $updateData
     * @return array
     */
    public function updateStudent($email, array $updateData)
    {
        $updateData['email'] = $email;
        
        $response = Http::post("{$this->baseUrl}/update-student/", $updateData);
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to update student: ' . $response->body());
    }

    /**
     * Send custom email template to all students
     * 
     * @param string $subject
     * @param string $message Use placeholders: {name}, {course_name}, {link}
     * @return array
     */
    public function sendEmailTemplate($subject, $message)
    {
        $response = Http::post("{$this->baseUrl}/send-template/", [
            'subject' => $subject,
            'message' => $message
        ]);
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to send template: ' . $response->body());
    }

    /**
     * Delete a single student by ID
     * 
     * @param int $studentId
     * @return array
     */
    public function deleteStudent($studentId)
    {
        $response = Http::delete("{$this->baseUrl}/delete-student/{$studentId}/");
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to delete student: ' . $response->body());
    }

    /**
     * Delete all students
     * 
     * @return array
     */
    public function deleteAllStudents()
    {
        $response = Http::delete("{$this->baseUrl}/delete-all/");
        
        if ($response->successful()) {
            return $response->json();
        }
        
        throw new \Exception('Failed to delete all students: ' . $response->body());
    }
}

// ============================================
// USAGE EXAMPLES IN LARAVEL CONTROLLER
// ============================================

namespace App\Http\Controllers;

use App\Services\EmailAutomationService;
use Illuminate\Http\Request;

class StudentController extends Controller
{
    private $emailService;

    public function __construct(EmailAutomationService $emailService)
    {
        $this->emailService = $emailService;
    }

    /**
     * Display all students
     */
    public function index()
    {
        try {
            $students = $this->emailService->getAllStudents();
            return view('students.index', compact('students'));
        } catch (\Exception $e) {
            return back()->with('error', $e->getMessage());
        }
    }

    /**
     * Upload Excel file
     */
    public function uploadExcel(Request $request)
    {
        $request->validate([
            'file' => 'required|file|mimes:xlsx,xls'
        ]);

        try {
            $filePath = $request->file('file')->getRealPath();
            $replaceAll = $request->has('replace_all');
            
            $result = $this->emailService->uploadExcel($filePath, $replaceAll);
            
            return back()->with('success', $result['message']);
        } catch (\Exception $e) {
            return back()->with('error', $e->getMessage());
        }
    }

    /**
     * Add new student
     */
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required|string',
            'email' => 'required|email',
            'mobile' => 'nullable|string',
            'course_name' => 'required|string',
            'link' => 'required|url'
        ]);

        try {
            $result = $this->emailService->addStudent($request->all());
            return response()->json($result, 201);
        } catch (\Exception $e) {
            // Check if duplicate
            if (strpos($e->getMessage(), 'Duplicate email') !== false) {
                // Ask user if they want to update
                return response()->json([
                    'error' => 'duplicate',
                    'message' => $e->getMessage(),
                    'email' => $request->email
                ], 409);
            }
            
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    /**
     * Update existing student
     */
    public function update(Request $request, $email)
    {
        $request->validate([
            'name' => 'required|string',
            'mobile' => 'nullable|string',
            'course_name' => 'required|string',
            'link' => 'required|url'
        ]);

        try {
            $result = $this->emailService->updateStudent($email, $request->all());
            return response()->json($result);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    /**
     * Send email template
     */
    public function sendTemplate(Request $request)
    {
        $request->validate([
            'subject' => 'required|string',
            'message' => 'required|string'
        ]);

        try {
            $result = $this->emailService->sendEmailTemplate(
                $request->subject,
                $request->message
            );
            
            return back()->with('success', $result['message']);
        } catch (\Exception $e) {
            return back()->with('error', $e->getMessage());
        }
    }

    /**
     * Delete student
     */
    public function destroy($id)
    {
        try {
            $result = $this->emailService->deleteStudent($id);
            return response()->json($result);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    /**
     * Delete all students
     */
    public function destroyAll()
    {
        try {
            $result = $this->emailService->deleteAllStudents();
            return back()->with('success', $result['message']);
        } catch (\Exception $e) {
            return back()->with('error', $e->getMessage());
        }
    }
}

// ============================================
// LARAVEL ROUTES (routes/web.php)
// ============================================

/*
use App\Http\Controllers\StudentController;

Route::prefix('students')->group(function () {
    Route::get('/', [StudentController::class, 'index'])->name('students.index');
    Route::post('/upload', [StudentController::class, 'uploadExcel'])->name('students.upload');
    Route::post('/', [StudentController::class, 'store'])->name('students.store');
    Route::put('/{email}', [StudentController::class, 'update'])->name('students.update');
    Route::post('/send-template', [StudentController::class, 'sendTemplate'])->name('students.send-template');
    Route::delete('/{id}', [StudentController::class, 'destroy'])->name('students.destroy');
    Route::delete('/', [StudentController::class, 'destroyAll'])->name('students.destroy-all');
});
*/

// ============================================
// BLADE VIEW EXAMPLE (resources/views/students/index.blade.php)
// ============================================

/*
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>Students Management</h1>
    
    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif
    
    @if(session('error'))
        <div class="alert alert-danger">{{ session('error') }}</div>
    @endif
    
    <!-- Upload Excel -->
    <form action="{{ route('students.upload') }}" method="POST" enctype="multipart/form-data">
        @csrf
        <input type="file" name="file" required>
        <label>
            <input type="checkbox" name="replace_all"> Replace all existing data
        </label>
        <button type="submit">Upload Excel</button>
    </form>
    
    <!-- Add Student Form -->
    <form action="{{ route('students.store') }}" method="POST">
        @csrf
        <input type="text" name="name" placeholder="Name" required>
        <input type="email" name="email" placeholder="Email" required>
        <input type="text" name="mobile" placeholder="Mobile">
        <input type="text" name="course_name" placeholder="Course Name" required>
        <input type="url" name="link" placeholder="Link" required>
        <button type="submit">Add Student</button>
    </form>
    
    <!-- Students Table -->
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            @foreach($students as $student)
            <tr>
                <td>{{ $student['id'] }}</td>
                <td>{{ $student['name'] }}</td>
                <td>{{ $student['email'] }}</td>
                <td>{{ $student['course_name'] }}</td>
                <td>
                    @if($student['template_sent'])
                        <span class="badge badge-success">✓ Sent</span>
                    @else
                        <span class="badge badge-warning">⏳ Pending</span>
                    @endif
                </td>
                <td>
                    <form action="{{ route('students.destroy', $student['id']) }}" method="POST">
                        @csrf
                        @method('DELETE')
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
    
    <!-- Send Template -->
    <form action="{{ route('students.send-template') }}" method="POST">
        @csrf
        <input type="text" name="subject" placeholder="Email Subject" required>
        <textarea name="message" placeholder="Message (use {name}, {course_name}, {link})" required></textarea>
        <button type="submit">Send to All Students</button>
    </form>
</div>
@endsection
*/
