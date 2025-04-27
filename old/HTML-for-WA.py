<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Exercise Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8">Language Exercise Generator</h1>
        
        <!-- Загрузка словаря -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 class="text-xl font-semibold mb-4">Upload Vocabulary</h2>
            <form id="vocabularyForm" class="space-y-4">
                <input type="file" accept=".csv,.txt" class="block w-full">
                <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
                    Upload
                </button>
            </form>
        </div>
        
        <!-- Генерация упражнений -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 class="text-xl font-semibold mb-4">Generate Exercises</h2>
            <form id="exerciseForm" class="space-y-4">
                <div>
                    <label class="block mb-2">Words (one per line):</label>
                    <textarea class="w-full h-32 border p-2 rounded" required></textarea>
                </div>
                <div>
                    <label class="block mb-2">Exercise Types:</label>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <input type="checkbox" value="gap_fill" checked>
                            <span class="ml-2">Gap Fill</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" value="paraphrase" checked>
                            <span class="ml-2">Paraphrase</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" value="matching" checked>
                            <span class="ml-2">Matching</span>
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" value="translation" checked>
                            <span class="ml-2">Translation</span>
                        </label>
                    </div>
                </div>
                <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">
                    Generate
                </button>
            </form>
            <div id="exerciseResults" class="mt-4"></div>
        </div>
        
        <!-- Анализ эссе -->
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold mb-4">Essay Analysis</h2>
            <form id="essayForm" class="space-y-4">
                <div>
                    <label class="block mb-2">Essay Text:</label>
                    <textarea class="w-full h-48 border p-2 rounded" required></textarea>
                </div>
                <button type="submit" class="bg-purple-500 text-white px-4 py-2 rounded">
                    Analyze
                </button>
            </form>
            <div id="essayResults" class="mt-4"></div>
        </div>
    </div>
    
    <script>
        // Функции для работы с API
        async function uploadVocabulary(formData) {
            const response = await fetch('/api/upload_vocabulary', {
                method: 'POST',
                body: formData
            });
            return response.json();
        }
        
        async function generateExercises(vocabulary, types) {
            const response = await fetch('/api/generate_exercises', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ vocabulary, types })
            });
            return response.json();
        }
        
        async function analyzeEssay(text) {
            const response = await fetch('/api/analyze_essay', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });
            return response.json();
        }
        
        // Обработчики форм
        document.getElementById('vocabularyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            formData.append('file', e.target.querySelector('input[type="file"]').files[0]);
            
            try {
                const result = await uploadVocabulary(formData);
                alert(result.message);
            } catch (error) {
                alert('Error uploading vocabulary');
            }
        });
        
        document.getElementById('exerciseForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const vocabulary = e.target.querySelector('textarea').value.split('\n').filter(w => w.trim());
            const types = Array.from(e.target.querySelectorAll('input[type="checkbox"]:checked'))
                              .map(cb => cb.value);
            
            try {
                const exercises = await generateExercises(vocabulary, types);
                displayExercises(exercises);
            } catch (error) {
                alert('Error generating exercises');
            }
        });
        
        document.getElementById('essayForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = e.target.querySelector('textarea').value;
            
            try {
                const analysis = await analyzeEssay(text);
                displayEssayAnalysis(analysis);
            } catch (error) {
                alert('Error analyzing essay');
            }
        });
        
        // Функции отображения результатов
        function displayExercises(exercises) {
            const container = document.getElementById('exerciseResults');
            container.innerHTML = ''; // Clear previous results
            
            Object.entries(exercises).forEach(([type, items]) => {
                const section = document.createElement('div');
                section.className = 'mb-4';
                section.innerHTML = `
                    <h3 class="font-semibold mt-4">${type}</h3>
                    <div class="pl-4">
                        ${items.map(item => `<p class="my-2">${JSON.stringify(item)}</p>`).join('')}
                    </div>
                `;
                container.appendChild(section);
            });
        }
        
        function displayEssayAnalysis(analysis) {
            const container = document.getElementById('essayResults');
            container.innerHTML = `
                <div class="border-t mt-4 pt-4">
                    <h3 class="font-semibold">Corrected Text:</h3>
                    <div class="whitespace-pre-wrap mt-2">${analysis.corrected_text}</div>
                    
                    <h3 class="font-semibold mt-4">Matches:</h3>
                    <ul class="list-disc pl-5 mt-2">
                        ${Object.entries(analysis.matches)
                            .map(([word, contexts]) => `
                                <li class="my-1">
                                    <strong>${word}</strong>: ${contexts.join('; ')}
                                </li>
                            `).join('')}
                    </ul>
                </div>
            `;
        }
    </script>
</body>
</html>
