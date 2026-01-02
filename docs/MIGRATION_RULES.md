# Documentation Migration Rules

> **Purpose**: Clear guidelines for migrating existing documentation to the new structure
> **Agent**: Agent C (Content Migrator)
> **Created**: 2026-01-02
> **Status**: Active

---

## Overview

This document defines the rules and procedures for migrating existing documentation from the old structure to the new, organized system in `/docs/`.

### Migration Principles

1. **Preserve All Content**: No valuable content should be lost
2. **Enhance Structure**: Apply templates for consistency
3. **Add Metadata**: Use YAML frontmatter for discoverability
4. **Create Cross-References**: Link related documents
5. **Validate Links**: Ensure all links work after migration

---

## Directory Mapping

### Source → Destination Mapping

```
OLD STRUCTURE                          NEW STRUCTURE
================================================================================
/learning_notes/00_learning_strategy.md
                                       → /docs/01_learning_strategy.md

/learning_notes/ai_builder_context.md  → /docs/00_getting_started.md (consolidated)

/learning_notes/weekN/*.md             → /docs/weeks/weekN/overview.md (concepts)
                                       → /docs/weeks/weekN/implementation.md (technical)
                                       → /docs/weeks/weekN/reflection.md (learning)

/weekN/writeup.md                      → /docs/weeks/weekN/ (extract content)
                                       → /weekN/writeup.md (submission deliverable)

/weekN/README.md                       → /docs/weeks/weekN/overview.md (if conceptual)
                                       → /docs/weeks/weekN/implementation.md (if technical)

/claude-best-practices/                → /claude-best-practices/ (NO CHANGE)
                                       → Cross-reference from /docs/patterns/
```

---

## Content Type Classification

Before migrating, classify each document by type:

### Type 1: Concept Documentation
**Indicators**:
- Title contains: "Overview", "Concepts", "Introduction", "Theory"
- Content: Learning objectives, key concepts, prerequisites
- Location: `/learning_notes/weekN/` files with theoretical content

**Destination**: `/docs/weeks/weekN/overview.md`

**Transformation**:
1. Apply `weekly_overview.md` template
2. Extract learning objectives
3. List key concepts with descriptions
4. Add prerequisites and resources sections
5. Add frontmatter with metadata

### Type 2: Implementation Documentation
**Indicators**:
- Title contains: "Implementation", "Technical", "Setup", "Configuration"
- Content: Code examples, architecture, technical decisions
- Location: `/weekN/` directories with technical content

**Destination**: `/docs/weeks/weekN/implementation.md`

**Transformation**:
1. Apply `weekly_implementation.md` template
2. Extract technical decisions
3. Document code structure
4. List challenges and solutions
5. Add testing strategy section

### Type 3: Reflection Documentation
**Indicators**:
- Title contains: "Reflection", "Lessons Learned", "What I Learned"
- Content: Personal insights, mistakes, growth
- Location: `/weekN/writeup.md` reflection sections

**Destination**: `/docs/weeks/weekN/reflection.md`

**Transformation**:
1. Apply `weekly_reflection.md` template
2. Extract technical skills learned
3. Document AI engineering concepts
4. List mistakes and prevention strategies
5. Add time allocation analysis

### Type 4: Deliverable Documentation
**Indicators**:
- Submission files, grading checklists
- Links to code repositories
- Self-assessment criteria

**Destination**: `/weekN/writeup.md` (keep in place)

**Transformation**:
1. Apply `weekly_deliverable.md` template
2. Add links to `/docs/weeks/weekN/` documentation
3. Include submission checklist
4. Add quick links to overview, implementation, reflection

---

## Migration Procedure

### Step 1: Inventory and Classify

For each week (1-8):

1. **List all documentation files**:
   ```bash
   find /learning_notes/weekN/ -name "*.md"
   find /weekN/ -name "*.md"
   ```

2. **Classify each file** by content type:
   - [ ] Concept → `overview.md`
   - [ ] Implementation → `implementation.md`
   - [ ] Reflection → `reflection.md`
   - [ ] Deliverable → `writeup.md`

3. **Create migration manifest**:
   ```markdown
   ## Week N Migration Manifest

   | Source File | Type | Destination | Status |
   |-------------|------|-------------|--------|
   | /path/to/file1.md | Concept | /docs/weeks/weekN/overview.md | [ ] |
   | /path/to/file2.md | Implementation | /docs/weeks/weekN/implementation.md | [ ] |
   ```

### Step 2: Create Target Directories

```bash
# For each week
mkdir -p /docs/weeks/weekN/
```

### Step 3: Apply Templates and Migrate Content

For each destination file:

1. **Copy template** to destination
2. **Update frontmatter**:
   ```yaml
   ---
   week: N
   title: "Week N: [Actual Title]"
   type: [concept|implementation|reflection|deliverable]
   status: [draft|active|completed]
   created: YYYY-MM-DD
   updated: 2026-01-02
   related:
     - week:N:overview.md
     - week:N:implementation.md
     - week:N:reflection.md
   tags: [week-N, type]
   ---
   ```

3. **Extract and organize content**:
   - Read source file(s)
   - Identify relevant sections
   - Copy content to appropriate template sections
   - Preserve code blocks, diagrams, and examples

4. **Enhance content**:
   - Add breadcrumb navigation
   - Add cross-references to related documents
   - Add "Quick Links" section
   - Preserve original formatting

### Step 4: Update Links

1. **Internal cross-references**:
   - Update relative paths
   - Example: `../weekN/file.md` → `../../weeks/weekN/file.md`

2. **External links**:
   - Validate all external URLs
   - Fix or remove broken links

3. **Image references**:
   - Update image paths if needed
   - Ensure images are accessible

### Step 5: Validation

For each migrated file:

- [ ] Template properly applied
- [ ] Frontmatter complete and valid
- [ ] All content preserved
- [ ] Cross-references added
- [ ] Internal links validated
- [ ] Breadcrumb navigation present
- [ ] "Quick Links" section added
- [ ] Markdown formatting correct
- [ ] Code blocks properly formatted
- [ ] Tables properly formatted

---

## Content-Specific Rules

### Rule 1: Learning Strategy Content

**Source**: `/learning_notes/00_learning_strategy.md`

**Destination**: `/docs/01_learning_strategy.md`

**Transformation**:
- Keep existing structure
- Add frontmatter metadata
- Add breadcrumb navigation
- Add cross-references to Getting Started guide
- Link to relevant patterns

### Rule 2: AI Builder Context

**Source**: `/learning_notes/ai_builder_context.md`

**Destination**: Consolidate into `/docs/00_getting_started.md`

**Transformation**:
- Merge with other getting started content
- Create sections: "AI Engineering Mindset", "Course Approach", "Tooling"
- Add frontmatter
- Add cross-references

### Rule 3: Week-Specific Learning Notes

**Source**: `/learning_notes/weekN/*.md` (multiple files)

**Destination**: Consolidate into `/docs/weeks/weekN/overview.md`

**Transformation**:
- Identify main concepts file
- Identify supplementary notes
- Merge into single overview document
- Use template structure
- Preserve all valuable content

### Rule 4: Writeup Files

**Source**: `/weekN/writeup.md`

**Destinations**:
- Extract implementation → `/docs/weeks/weekN/implementation.md`
- Extract reflection → `/docs/weeks/weekN/reflection.md`
- Update deliverable → `/weekN/writeup.md`

**Transformation**:
1. Read existing writeup
2. Identify sections by content type
3. Extract to appropriate destination
4. Update original writeup with template
5. Add links to extracted documentation

### Rule 5: README Files

**Source**: `/weekN/README.md`

**Destination**: `/docs/weeks/weekN/overview.md` or `implementation.md`

**Decision Criteria**:
- If conceptual → `overview.md`
- If technical → `implementation.md`
- If mixed → split between both

---

## Special Cases

### Case 1: Content Spanning Multiple Types

**Scenario**: A single file contains both concepts and implementation

**Solution**:
1. Split content by section
2. Create multiple destination files
3. Add cross-references between them
4. Preserve narrative flow

**Example**:
```markdown
# Original File
## Concepts
[Concept content]

## Implementation
[Implementation content]

# After Migration
# overview.md contains "Concepts"
# implementation.md contains "Implementation"
# Both files cross-reference each other
```

### Case 2: Duplicate or Similar Content

**Scenario**: Multiple weeks contain similar pattern descriptions

**Solution**:
1. Extract common pattern to `/docs/patterns/pattern-name.md`
2. In each week's documentation:
   - Brief description
   - Link to pattern: "See [Pattern Name](../../patterns/pattern-name.md)"
   - Week-specific application details

### Case 3: Outdated or Superseded Content

**Scenario**: Old documentation that's no longer relevant

**Solution**:
1. Evaluate historical value
2. If valuable for learning: keep in `/docs/archive/`
3. If not valuable: note in migration log, skip
4. Document decision in migration manifest

### Case 4: Missing Content

**Scenario**: Template requires content that doesn't exist in source

**Solution**:
1. Use placeholder: "[To be added]"
2. Add comment: "[TODO: Add this section]"
3. Note in migration manifest
4. Don't invent content - leave explicit placeholders

---

## Validation Criteria

### Completeness Check

For each week, verify:

- [ ] All source files accounted for
- [ ] All content migrated (or intentionally skipped with reason)
- [ ] All templates applied
- [ ] All frontmatter complete
- [ ] All cross-references added

### Quality Check

For each migrated file:

- [ ] Markdown renders correctly
- [ ] Code blocks have proper syntax highlighting
- [ ] Tables are properly formatted
- [ ] Links work (internal and external)
- [ ] Images load (if applicable)
- [ ] Spelling and grammar checked
- [ ] Technical accuracy verified

### Consistency Check

Across all migrated files:

- [ ] Breadcrumb navigation format consistent
- [ ] Frontmatter schema consistent
- [ ] Section ordering follows template
- [ ] Cross-reference format consistent
- [ ] Date format consistent (YYYY-MM-DD)

---

## Automated Validation Script

Create `/docs/scripts/validate_migration.sh`:

```bash
#!/bin/bash

# Check for required files
echo "Checking for required files..."

for week in {01..08}; do
    echo "Checking Week $week..."

    # Check for required documentation
    if [ -f "/docs/weeks/week$week/overview.md" ]; then
        echo "  ✓ overview.md exists"
    else
        echo "  ✗ overview.md missing"
    fi

    if [ -f "/docs/weeks/week$week/implementation.md" ]; then
        echo "  ✓ implementation.md exists"
    else
        echo "  ✗ implementation.md missing"
    fi

    if [ -f "/docs/weeks/week$week/reflection.md" ]; then
        echo "  ✓ reflection.md exists"
    else
        echo "  ✗ reflection.md missing"
    fi

    # Validate frontmatter
    echo "  Validating frontmatter..."
    # Add frontmatter validation logic here
done

echo "Validation complete!"
```

---

## Rollback Plan

If migration needs to be reverted:

1. **Stop migration** immediately
2. **Document issues** encountered
3. **Restore from backup**:
   ```bash
   git checkout backup-branch-before-migration
   ```
4. **Fix migration rules** based on issues
5. **Retry migration** with updated rules

**Pre-migration backup**:
```bash
git checkout -b backup-before-doc-migration
git commit -am "Backup before documentation migration"
git checkout master
```

---

## Migration Checklist

### Pre-Migration
- [ ] All templates created and reviewed
- [ ] INDEX.md finalized
- [ ] MIGRATION_RULES.md reviewed and approved
- [ ] Backup branch created
- [ ] Migration manifest prepared for each week

### During Migration
- [ ] Follow content classification rules
- [ ] Apply templates correctly
- [ ] Preserve all valuable content
- [ ] Update all links
- [ ] Validate each file as it's migrated
- [ ] Update migration manifest

### Post-Migration
- [ ] Run validation script
- [ ] Check all internal links
- [ ] Verify all external links
- [ ] Test navigation from INDEX.md
- [ ] Review cross-references
- [ ] Update this MIGRATION_RULES.md with lessons learned

---

## Notes for Agent C (Content Migrator)

### Priorities
1. **Week 5** (most recent, active work)
2. **Week 1-4** (foundational content)
3. **Week 6-8** (if applicable)

### Common Pitfalls to Avoid
- Don't skip validation - it catches mistakes early
- Don't break existing links - update all references
- Don't lose content - when in doubt, keep it
- Don't mix content types - keep concepts separate from implementation
- Don't forget frontmatter - it enables automation

### When in Doubt
1. Preserve the content
2. Add a TODO comment
3. Document the decision in the migration manifest
4. Move on and return later

### Success Metrics
- All weeks have complete documentation (overview, implementation, reflection)
- All internal links work
- All templates properly applied
- Zero content loss
- Navigation flows from INDEX.md to any document in 3 clicks or less

---

**Migration Progress**: Not started
**Last Updated**: 2026-01-02
**Next Review**: After first week migration

*[This document should be updated as migration progresses with lessons learned]*
