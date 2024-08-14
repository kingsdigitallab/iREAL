export type Node = {
	_node_content: string;
	_node_type: string;
	doc_id: string;
	document_id: string;
	document_title: string;
	diseases?: string[];
	events?: string[];
	excerpt_keywords: string;
	file: string;
	geo?: number[];
	locations?: string[];
	media?: string[];
	next_section_summary?: string;
	organizations?: string[];
	persons?: string[];
	prev_section_summary?: string;
	questions_this_excerpt_can_answer: string;
	ref_doc_id: string;
	school: string;
	section_summary: string;
	times?: string[];
	topics: string[];
};

export type Result = {
	nodes: Node[];
	schools: School[];
	schoolsNames: string[];
	keywords: Facet[];
	organisations: { organisation: string; count: number }[];
	people: { person: string; count: number }[];
	places: { place: string; count: number }[];
	topics: Facet[];
};

export type School = {
	name: string;
	slug: string;
	keywords: string[];
	topics: string[];
};

export type Facet = {
	name: string;
	count: number;
};
