"""Local read-only UI for the verified Maple Freight dispatch report."""
import streamlit as st
from report import build, REFERENCE, BACKFILL_RECEIVED, rows, fmt

st.set_page_config(page_title='Maple Freight | Dispatch', page_icon='🚚', layout='wide')
show_backfill = st.sidebar.checkbox('Include 6:47 p.m. Hamilton backfill', value=True)
report, eligible = build(include_backfill=show_backfill)
sections = report.split('### ')[1:]
issues = []
for section in sections:
    title, _, body = section.partition('\n')
    if '## Export checks' in body:
        body = body.split('## Export checks')[0]
    issues.append((title, body.strip()))

st.title('🚚 Maple Freight · Dispatch Action Queue')
st.caption(f'Original snapshot: {fmt(REFERENCE)} · ' + (f'Updated view: {fmt(BACKFILL_RECEIVED)}' if show_backfill else 'Original view') + ' · Read-only recommendations')
col1, col2, col3 = st.columns(3)
col1.metric('Eligible alerts', f'{len(eligible):,}')
col2.metric('Selected actions', len(issues))
col3.metric('Daily team capacity', 'Up to 10')
st.info('Curated three-case baseline, not exhaustive fleet-wide triage. Backfill events happened earlier but arrived at 6:47 p.m.; toggle to compare the original 6 p.m. view.')

st.subheader('Priority actions')
for title, body in issues:
    with st.container(border=True):
        st.markdown(f'#### {title}')
        paragraphs = body.split('**Supporting alerts:**')
        st.markdown(paragraphs[0])
        if len(paragraphs) > 1:
            with st.expander('Inspect alert IDs, fault codes, timestamps and shop records'):
                st.markdown('**Supporting alerts:**' + paragraphs[1])

with st.expander('Export quality, ranking rules, exclusions and uncertainty'):
    st.markdown('## Export checks' + report.split('## Export checks', 1)[1])

st.subheader('Inspect original source records')
st.caption('Browse the supplied CSVs. These are source records, not synthetic examples.')
choice = st.selectbox('Data file', ['alerts.csv', 'hamilton_backfill.csv', 'vehicles.csv', 'dtc_reference.csv', 'work_orders.csv'])
source = rows(choice)
if choice == 'alerts.csv':
    vehicle = st.text_input('Filter alerts by vehicle ID (optional)', '').strip().upper()
    if vehicle:
        source = [r for r in source if r['vehicle_id'] == vehicle]
st.caption(f'{len(source)} matching records')
st.dataframe(source, use_container_width=True, hide_index=True)

st.download_button('Download evidence report (.md)', report, file_name='BACKFILL_REPORT.md' if show_backfill else 'DISPATCH_REPORT.md', mime='text/markdown')
