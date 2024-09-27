import { dev } from '$app/environment';

export const title = 'iREAL';
export const description =
	'Inclusive Requirements Elicitation for AI in Libraries to Support Respectful Management of Indigenous Knowledges';
export const url = dev ? 'http://localhost:5173/' : 'https://kingsdigitallab.github.io/ireal/';
export const apiUrl = dev
	? 'http://localhost:8000/api/query'
	: 'https://ireal.kdl.kcl.ac.uk/api/query';

export const promptTemplate = `

Context information is below:
---------------------
{context_str}
---------------------
Given this information, please answer the question: {query_str}
`;

export const github = 'https://github.com/kingsdigitallab/iREAL';

export const entityFields = ['locations', 'organizations', 'persons'];

export const topics = [
	'education policies',
	'assimilation',
	'cultural suppression',
	'mission schools',
	'government schools',
	'Aboriginal reserves',
	'segregation',
	'curriculum',
	'language preservation',
	'traditional knowledge',
	'teacher training',
	'attendance rates',
	'funding issues',
	'racism',
	'health conditions',
	'living conditions',
	'vocational training',
	'religious instruction',
	'child removal policies',
	'Indigenous resistance'
];
